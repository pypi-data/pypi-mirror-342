from info.toolbox.networks._frame import tch, nn, GeneratorType, Module, FuncTools, T, Null, _is_valid_stop_cond
from info.toolbox.networks.classic import _FullConnected
from info.basic.functions import assert_info_raiser
from info.basic.core import TrialDict
from info import docfunc as doc
from typing import Callable, Optional, Literal, Union, Generator, Any
import numpy as np
from warnings import warn
mha = getattr(nn, 'MultiheadAttention')
_func = getattr(nn, 'functional')
softmax, dropout = [getattr(_func, _) for _ in ['softmax', 'dropout']]
_data_basic = Union[tch.Tensor, np.ndarray, Generator]
_Tensor = Union[_data_basic, tuple[_data_basic, Optional[Any]]]
_emb_func_type = dict[Literal['in', 'out', 'endmost'], Optional[Callable]]


def _as_one_hot(x: tch.Tensor, dict_length: int) -> tch.Tensor:
    one_hot = tch.zeros(*x.shape, dict_length, device=x.device)
    one_hot.scatter_(-1, x.unsqueeze(-1), 1)
    return one_hot


def _to_tensor(x: Optional[Union[np.ndarray, tch.Tensor, GeneratorType]]) -> Optional[tch.Tensor]:
    if isinstance(x, np.ndarray):
        res = tch.from_numpy(x)
    elif isinstance(x, GeneratorType):
        res = tch.from_numpy(np.stack([_ for _ in x]))
    else:
        res = x
    return res


def _attentions(*, d_model: int, num_heads: int, attn_init: dict = None, attn_forward: dict = None):
    # https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
    # Attention Is All You Need: https://arxiv.org/abs/1706.03762
    _attn_init = dict() if attn_init is None else attn_init
    _attn_forward = dict() if attn_forward is None else attn_forward
    attn_init = {**{'dropout': 0.0, 'bias': True, 'add_bias_kv': False, 'add_zero_attn': False, 'kdim': None,
                    'vdim': None, 'batch_first': True}, **_attn_init}
    attn_init.update(embed_dim=d_model, num_heads=num_heads)
    attn_forward = {**{'need_weights': True, 'attn_mask': None, 'average_attn_weights': True,
                       'is_causal': False}, **_attn_forward}
    return mha(**attn_init), attn_forward


def _lambda_module_dict(forward: Callable, modules: nn.ModuleDict):
    _lambda_module = type('_lambda_module', (nn.ModuleDict,), {'forward': forward})
    return _lambda_module(modules)


def _get_respective_qkv(_d_model: int, _num_heads: int, _attn_call: mha, _attn_config: dict, _batch_size: int,
                        _seq_len_q: int, _seq_len_k: int, _q_like: tch.Tensor, _k_like: tch.Tensor,
                        _v_like: tch.Tensor):
    _head_dim = _d_model // _num_heads
    _in_weight_q, _in_bias_q = (_attn_call.in_proj_weight[:_d_model, :],
                                _attn_call.in_proj_bias[: _d_model])
    _in_weight_k, _in_bias_k = (_attn_call.in_proj_weight[_d_model: _d_model * 2, :],
                                _attn_call.in_proj_bias[_d_model: _d_model * 2])
    _in_weight_v, _in_bias_v = (_attn_call.in_proj_weight[_d_model * 2:, :],
                                _attn_call.in_proj_bias[_d_model * 2:])

    if all([getattr(_attn_call, _) is not None for _ in ['q_proj_weight', 'k_proj_weight', 'v_proj_weight']]):
        _in_weight_q, _in_weight_k, _in_weight_v = (_attn_call.q_proj_weight, _attn_call.k_proj_weight,
                                                    _attn_call.v_proj_weight)  # compatibility for unequal embedding
    q = ((_q_like @ _in_weight_q.T) + _in_bias_q).contiguous()
    k = ((_k_like @ _in_weight_k.T) + _in_bias_k).contiguous()
    v = ((_v_like @ _in_weight_v.T) + _in_bias_v).contiguous()
    return q, k, v


def _generic_relative_attention_forward(_d_model: int, _num_heads: int, _attn_call: mha, _attn_config: dict,
                                        _batch_size: int, _seq_len_q: int, _seq_len_k: int, _max_relative: int,
                                        _relative_pos_emb: tch.Tensor, _q_like: tch.Tensor, _k_like: tch.Tensor,
                                        _v_like: tch.Tensor, _msk_like: tch.Tensor = None) -> tch.Tensor:
    _head_dim = _d_model // _num_heads
    q, k, v = _get_respective_qkv(_d_model, _num_heads, _attn_call, _attn_config, _batch_size, _seq_len_q, _seq_len_k,
                                  _q_like, _k_like, _v_like)
    q, k, v = [v1.view(_batch_size, v2, _num_heads, _head_dim).transpose(1, 2) for v1, v2
               in zip((q, k, v), (_seq_len_q, _seq_len_k, _seq_len_k))]
    attn_scores = tch.matmul(q, k.transpose(-2, -1)) / tch.clip(_head_dim ** 0.5, min=1e-4)
    _augment = _relative_pos_emb[(tch.arange(_seq_len_q)[:, None] -
                                  tch.arange(_seq_len_k)[None, :]).clip(-_max_relative, _max_relative)
                                 + _max_relative]  # Music Transformer: https://arxiv.org/abs/1809.04281
    _augment = _augment.permute(2, 0, 1).unsqueeze(0).unsqueeze(0).expand(_batch_size, _num_heads,
                                                                          -1, -1, -1).sum(dim=2)
    attn_scores = attn_scores + _augment

    if _msk_like is not None:

        _tmp = _msk_like.unsqueeze(1).unsqueeze(2)
        if _seq_len_q == _seq_len_k:  # branch for mainly self attention
            causal_mask = tch.triu(tch.ones(_seq_len_q, _seq_len_k, device=q.device), diagonal=1).bool()
            attn_scores.masked_fill(causal_mask | _tmp, float('-inf'))
            # attn_scores = attn_scores.masked_fill(_tmp * _tmp.transpose(-1, -2), float('-inf'))
        else:  # other, branch for cross attention
            attn_scores = attn_scores.masked_fill(_tmp, float('-inf'))

    attn_weights = softmax(attn_scores.masked_fill(attn_scores == float('-inf'), -1e4), dim=-1)
    attn_weights = dropout(attn_weights, p=_attn_call.dropout, training=_attn_call.training)
    _export = tch.matmul(attn_weights, v)
    _export = _export.transpose(1, 2).reshape(_batch_size, _seq_len_q, -1)

    return _attn_call.out_proj(_export)


def _apply_rotation(q: tch.Tensor,  k: tch.Tensor, freq: tch.Tensor) -> tuple[tch.Tensor, tch.Tensor]:
    q_c, k_c = (tch.view_as_complex(q.float().reshape(*q.shape[:-1], -1, 2)),
                tch.view_as_complex(k.float().reshape(*k.shape[:-1], -1, 2)))
    _freq = freq.unsqueeze(0).unsqueeze(2)
    q_r, k_r = q_c * _freq, k_c * _freq if q.shape == k.shape else k_c  # support cross attention, no use for k_c
    return tch.view_as_real(q_r).flatten(3).type_as(q), tch.view_as_real(k_r).flatten(3).type_as(k)


def _feed_forward_neural(d_model: int, d_feed_forward: int, _activation: Callable = nn.ReLU, _dropout: float = None):
    _comp = [nn.Linear(d_model, d_feed_forward), _activation(), nn.Linear(d_feed_forward, d_model)]
    if _dropout is not None:
        _comp.append(nn.Dropout(_dropout))
    return nn.Sequential(*_comp)


def _factorize_int(n: int) -> tch.Tensor:
    numbers = tch.arange(1, n+1)
    return numbers[n % numbers == 0]


_voc_size_type = (lambda x: isinstance(x, dict) and len(x) == 2 and
                  all([k in ['in', 'out'] and isinstance(v, int) and v > 0 for k, v in x.items()]))
_refactor_num_heads = (lambda _d, _h: _h if (_d % _h == 0) else
                       [_msg := f'{_d} is indivisible by {_h}, reassign the value of num_heads',
                        _factors := _factorize_int(_d), _idx := int(tch.argmin((_factors - _h).abs())),
                        _res := int(_factors[_idx]), _msg := _msg + f' to {_res}',
                        warn(_msg), _res][-1])
_encoding_config = TrialDict(**{'max_length': 5000, 'base': 10000, 'max_relative': 3, 'theta': 10000.0, 'start_pos': 0})


class _Positional:

    def __init__(self, encoding_meth: str):
        _valid_type = ['sinusoid', 'trainable', 'relative', 'rotation']
        assert_info_raiser(encoding_meth in _valid_type,
                           ValueError(f'encoding method should be one of {_valid_type}'))
        self.encoding_meth = encoding_meth

    @property
    def embedding(self):  # implementation requirement: necessary materials (to be registered) for attention forward

        if self.encoding_meth == 'sinusoid':
            def func(_d_model: int, _max_len: int, _base: int = 10000) -> tch.Tensor:
                pos, div = (tch.arange(_max_len)[..., tch.newaxis].type(tch.float),
                            tch.exp(tch.tensor([_ // 2 for _ in tch.arange(_d_model)]) * 2 *
                                    (-tch.log(tch.tensor([_base])) / _d_model))[..., tch.newaxis])
                return tch.stack([tch.sin(tch.Tensor(_)) if i % 2 == 0 else tch.cos(tch.Tensor(_))
                                  for i, _ in enumerate((pos @ div.T).T)], dim=0).T
            return func

        elif self.encoding_meth == 'trainable':
            def func(_d_model: int, _max_len: int) -> tch.Tensor:
                return tch.rand(_max_len, _d_model) * 2 - 1
            return func

        elif self.encoding_meth == 'relative':

            def func(_d_model: int, _num_heads: int, _attn_call: mha, _attn_config: dict, _batch_size: int,
                     _seq_len_q: int, _seq_len_k: int, _max_relative: int, _relative_pos_emb: tch.Tensor,
                     _q_like: tch.Tensor, _k_like: tch.Tensor, _v_like: tch.Tensor,
                     _msk_like: tch.Tensor = None) -> tch.Tensor:
                return _generic_relative_attention_forward(_d_model, _num_heads, _attn_call, _attn_config, _batch_size,
                                                           _seq_len_q, _seq_len_k, _max_relative, _relative_pos_emb,
                                                           _q_like, _k_like, _v_like, _msk_like)

            return func

        elif self.encoding_meth == 'rotation':

            def func(_d_model: int, _num_heads: int, _max_len: int, _theta: float):
                _dim = _d_model // _num_heads
                freq = 1.0 / (_theta ** (tch.arange(0, _dim, 2)[: (_dim // 2)].float() / _dim))
                freq = tch.outer(tch.arange(_max_len, device=freq.device), freq).float()
                return tch.polar(tch.ones_like(freq), freq)

            return func

    @property
    def attentions(self):  # implementation requirement: support both self and cross attention forward

        if self.encoding_meth in ['sinusoid', 'trainable']:
            def func(_attn_call: mha, _attn_config: dict, q: tch.Tensor, k: tch.Tensor, v: tch.Tensor,
                     msk: tch.Tensor = None) -> tch.Tensor:
                if msk is not None:
                    _attn_config = {**_attn_config, **{'key_padding_mask': msk}}
                return _attn_call(q, k, v, **_attn_config)[0]
            return func

        elif self.encoding_meth == 'relative':  # the same as embedding function, no use

            def func(_d_model: int, _num_heads: int, _attn_call: mha, _attn_config: dict, _batch_size: int,
                     _seq_len_q: int, _seq_len_k: int, _max_relative: int, _relative_pos_emb: tch.Tensor,
                     _q_like: tch.Tensor, _k_like: tch.Tensor, _v_like: tch.Tensor,
                     _msk_like: tch.Tensor = None) -> tch.Tensor:
                return _generic_relative_attention_forward(_d_model, _num_heads, _attn_call, _attn_config, _batch_size,
                                                           _seq_len_q, _seq_len_k, _max_relative, _relative_pos_emb,
                                                           _q_like, _k_like, _v_like, _msk_like)

            return func

        elif self.encoding_meth == 'rotation':

            def func(_d_model: int, _num_heads: int, _attn_call: mha, _attn_config: dict, _batch_size: int,
                     _seq_len_q: int, _seq_len_k: int, _freq: tch.Tensor, _start_pos: int, _q_like: tch.Tensor,
                     _k_like: tch.Tensor, _v_like: tch.Tensor, _msk_like: tch.Tensor):
                _head_dim = _d_model // _num_heads
                q, k, v = _get_respective_qkv(_d_model, _num_heads, _attn_call, _attn_config, _batch_size, _seq_len_q,
                                              _seq_len_k, _q_like, _k_like, _v_like)
                q, k, v = [v1.view(_batch_size, v2, _num_heads, _head_dim) for v1, v2
                           in zip((q, k, v), (_seq_len_q, _seq_len_k, _seq_len_k))]
                q_r, k_r = _apply_rotation(q, k, _freq[_start_pos: _start_pos + _seq_len_q])

                _k_ptr = k_r if (_is_self_attn := _seq_len_q == _seq_len_k) else k
                attn_scores = tch.einsum("bqhd,bkhd->bhqk", q_r, _k_ptr) / tch.clip(_head_dim ** 0.5, min=1e-4)

                if _msk_like is not None:
                    if _is_self_attn:
                        batch_size, num_heads, query_len, key_len = attn_scores.shape
                        causal_msk = tch.triu(
                            tch.ones(query_len, key_len, device=attn_scores.device) * float('-inf'),
                            diagonal=1
                        ).view(1, 1, query_len, key_len).expand(batch_size, num_heads, -1, -1)
                        pd_msk = _msk_like.unsqueeze(1).unsqueeze(2).expand(-1, num_heads, query_len, -1)
                        pd_msk = pd_msk.float().masked_fill(pd_msk, float('-inf'))
                        _tmp = tch.minimum(causal_msk, pd_msk)
                        attn_scores = attn_scores + _tmp.nan_to_num_(nan=0.0, neginf=-1e9)
                    else:
                        _tmp = _msk_like.unsqueeze(1).unsqueeze(2)
                        attn_scores = attn_scores.masked_fill(_tmp, float('-inf'))

                attn_weights = softmax(attn_scores, dim=-1)
                attn_weights = dropout(attn_weights, p=_attn_call.dropout, training=_attn_call.training)
                _export = tch.einsum("bhqk,bkhd->bqhd", attn_weights, v)
                _export = _export.reshape(_batch_size, _seq_len_q, -1)
                return _attn_call.out_proj(_export)

            return func


class _Transformer(Module):

    @FuncTools.params_setting(dimension_model=T[Null: int], num_heads=T[Null: int],
                              vocabulary_size=T[{'in': 10000, 'out': 8000}: _voc_size_type],
                              embedding_func=T[{'in': None, 'out': None, 'endmost': None}: _emb_func_type],
                              encoding_meth=T['sinusoid': Literal['sinusoid', 'trainable', 'relative', 'rotation']],
                              encoding_configs=T[_encoding_config: dict], dimension_feed_forward=T[2048: int],
                              activation=T[nn.ReLU: Callable], num_layers=T[6: Union[int, tuple[int, int]]],
                              attn_init=T[None: Optional[dict]], attn_forward=T[None: Optional[dict]],
                              dropout=T[0.1: float])
    def __init__(self, **params):
        super(_Transformer, self).__init__()
        (self._emb_func, self._encoding_meth, self._d_model, self._encoding_configs, self._num_l, self._d_ff, self._act,
         self._num_heads, self._attn_init, self._attn_forward, self._global_dropout, self._voc_size) = [
            params.get(k) for k in ['embedding_func', 'encoding_meth', 'dimension_model', 'encoding_configs',
                                    'num_layers', 'dimension_feed_forward', 'activation', 'num_heads', 'attn_init',
                                    'attn_forward', 'dropout', 'vocabulary_size']
        ]

        self._num_heads = _refactor_num_heads(self._d_model, self._num_heads)
        self._head_dim = self._d_model // self._num_heads
        self._num_l = [self._num_l, self._num_l] if isinstance(self._num_l, int) else self._num_l
        self._encoding_configs = _encoding_config.trial(**_m) if (_m := self._encoding_configs) else _encoding_config
        self._attn_init = ({'dropout': self._global_dropout, 'batch_first': True} if self._attn_init is None else
                           self._attn_init)
        self._emb_meta = _Positional(self._encoding_meth)
        self._pos_enc = nn.Sequential(self._get_positional_encoding(), nn.Dropout(self._global_dropout))
        self.encoder, self.decoder = self._encoder_chain(), self._decoder_chain()
        self.endmost = (self._emb_func.get('endmost') if self._emb_func.get('endmost') is not None else
                        _FullConnected(structure=[None, self._voc_size.get('out')], bias=True,
                                       activation=self._act, dropout=self._global_dropout))
        self._x_vectorizer = (self._emb_func.get('in') if self._emb_func.get('in') is not None else
                              nn.Embedding(self._voc_size.get('in'), self._d_model))
        self._y_vectorizer = (self._emb_func.get('out') if self._emb_func.get('out') is not None else
                              nn.Embedding(self._voc_size.get('out'), self._d_model))
        self.configs = self._default_train_configs()

    def _encoder(self):
        _modules = nn.ModuleDict()
        attn_call, attn_config = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                             attn_init=self._attn_init, attn_forward=self._attn_forward)
        _modules.update({'self_attn': attn_call, 'feed_forward': _feed_forward_neural(self._d_model, self._d_ff,
                                                                                      self._act, self._global_dropout),
                         '1st_norm': nn.LayerNorm(self._d_model), '2nd_norm': nn.LayerNorm(self._d_model)})
        _f_emb, _f_attn = self._emb_meta.embedding, self._emb_meta.attentions

        def _forward(cls: nn.ModuleDict, x: tch.Tensor, msk: tch.Tensor = None) -> tch.Tensor:
            if self._encoding_meth in ['sinusoid', 'trainable']:
                _tmp = _f_attn(cls.__getattr__('self_attn'), attn_config, x, x, x, msk)  # [32, 20, 512]
            elif self._encoding_meth == 'relative':
                batch_size, seq_len, _ = x.shape
                _max_emb_relative = self._encoding_configs.get('max_relative')
                if not hasattr(cls, _name := f'_relative_enc_emb_dim{seq_len}'):
                    cls.register_parameter(_name, nn.Parameter(tch.randn(2 * self._d_model - 1, self._head_dim)))
                _tmp = _f_emb(self._d_model, self._num_heads, cls.__getattr__('self_attn'), attn_config, batch_size,
                              seq_len, seq_len, _max_emb_relative, cls.__getattr__(_name), x, x, x, msk)
            else:  # rotation
                batch_size, seq_len, _ = x.shape
                _max_len, _theta, _start = [self._encoding_configs.get(_) for _ in ['max_length', 'theta', 'start_pos']]
                if not hasattr(cls, _name := f'_rotation_enc_emb_dim{seq_len}'):
                    cls.register_parameter(_name, nn.Parameter(_f_emb(self._d_model, self._num_heads, _max_len,
                                                                      _theta)))
                _tmp = _f_attn(self._d_model, self._num_heads, cls.__getattr__('self_attn'), attn_config, batch_size,
                               seq_len, seq_len, cls.__getattr__(_name), _start, x, x, x, msk)
            x = cls['1st_norm'](x + _tmp)
            _tmp = cls['feed_forward'](x)
            return cls['2nd_norm'](x + _tmp)

        return _lambda_module_dict(_forward, _modules)

    def _decoder(self):
        _modules = nn.ModuleDict()
        attn_call_1, attn_config_1 = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                                 attn_init=self._attn_init, attn_forward=self._attn_forward)
        attn_call_2, attn_config_2 = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                                 attn_init=self._attn_init, attn_forward=self._attn_forward)
        _modules.update({'self_attn': attn_call_1, 'cross_attn_base': attn_call_2,
                         'feed_forward': _feed_forward_neural(self._d_model, self._d_ff, self._act,
                                                              self._global_dropout),
                         '1st_norm': nn.LayerNorm(self._d_model), '2nd_norm': nn.LayerNorm(self._d_model),
                         '3rd_norm': nn.LayerNorm(self._d_model)})
        _f_emb, _f_attn = self._emb_meta.embedding, self._emb_meta.attentions

        def _forward(cls: nn.ModuleDict, y: tch.Tensor, m: tch.Tensor, x_msk: tch.Tensor = None,
                     y_msk: tch.Tensor = None) -> tch.Tensor:

            if self._encoding_meth in ['sinusoid', 'trainable']:
                _tmp = _f_attn(cls.__getattr__('self_attn'), attn_config_1, y, y, y, y_msk)  # [32, 15, 512]
            elif self._encoding_meth == 'relative':
                batch_size, seq_len, _ = y.shape
                _max_emb_relative = self._encoding_configs.get('max_relative')
                if not hasattr(cls, _name := f'_relative_dec_emb_dim{seq_len}'):
                    cls.register_parameter(_name, nn.Parameter(tch.randn(2 * self._d_model - 1, self._head_dim)))
                _tmp = _f_emb(self._d_model, self._num_heads, cls.__getattr__('self_attn'), attn_config_1, batch_size,
                              seq_len, seq_len, _max_emb_relative, cls.__getattr__(_name), y, y, y, y_msk)
            else:  # rotation
                batch_size, seq_len, _ = y.shape
                _max_len, _theta, _start = [self._encoding_configs.get(_) for _ in ['max_length', 'theta', 'start_pos']]
                if not hasattr(cls, _name := f'_rotation_dec_emb_dim{seq_len}'):
                    cls.register_parameter(_name, nn.Parameter(_f_emb(self._d_model, self._num_heads, _max_len,
                                                                      _theta)))
                _tmp = _f_attn(self._d_model, self._num_heads, cls.__getattr__('self_attn'), attn_config_1, batch_size,
                               seq_len, seq_len, cls.__getattr__(_name), _start, y, y, y, y_msk)

            y = cls['1st_norm'](y + _tmp)

            if self._encoding_meth in ['sinusoid', 'trainable']:
                _tmp = _f_attn(cls.__getattr__('cross_attn_base'), attn_config_2, y, m, m, x_msk)  # [32, 15, 512]
            elif self._encoding_meth == 'relative':
                batch_size, seq_len, _ = y.shape
                _, seq_len_cross, emb_dim_cross = m.shape
                _max_emb_relative = self._encoding_configs.get('max_relative')
                if not hasattr(cls, _name := f'_relative_dec_cross_dim{seq_len}_from_dim{seq_len_cross}'):
                    cls.register_parameter(_name, nn.Parameter(tch.randn(2 * self._d_model - 1, self._head_dim)))
                    _attn_cross_init = {**self._attn_init, **{'kdim': emb_dim_cross, 'vdim': emb_dim_cross}}
                    _attn_call, _ = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                                attn_init=_attn_cross_init, attn_forward=self._attn_forward)
                    cls.update({_name+'_attn': _attn_call})  # cross_attn_base no use here, with no grad
                _tmp = _f_emb(self._d_model, self._num_heads, cls.__getattr__(_name + '_attn'), attn_config_2,
                              batch_size, seq_len, seq_len_cross, _max_emb_relative, cls.__getattr__(_name), y, m, m,
                              x_msk)
            else:  # rotation
                batch_size, seq_len, _ = y.shape
                _, seq_len_cross, emb_dim_cross = m.shape
                _max_len, _theta, _start = [self._encoding_configs.get(_) for _ in ['max_length', 'theta', 'start_pos']]
                if not hasattr(cls, _name := f'_relative_dec_cross_dim{seq_len}_from_dim{seq_len_cross}'):
                    cls.register_parameter(_name, nn.Parameter(_f_emb(self._d_model, self._num_heads, _max_len,
                                                                      _theta)))
                    _attn_cross_init = {**self._attn_init, **{'kdim': emb_dim_cross, 'vdim': emb_dim_cross}}
                    _attn_call, _ = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                                attn_init=_attn_cross_init, attn_forward=self._attn_forward)
                    cls.update({_name + '_attn': _attn_call})
                _tmp = _f_attn(self._d_model, self._num_heads, cls.__getattr__(_name+'_attn'), attn_config_2,
                               batch_size, seq_len, seq_len_cross, cls.__getattr__(_name), _start, y, m, m, x_msk)

            y = cls['2nd_norm'](y + _tmp)
            return cls['3rd_norm'](y + cls['feed_forward'](y))

        return _lambda_module_dict(_forward, _modules)

    def _get_positional_encoding(self):
        _modules = nn.ModuleDict()
        _f_emb, _f_attn = self._emb_meta.embedding, self._emb_meta.attentions

        if self._encoding_meth in ['sinusoid', 'trainable']:

            def _forward(cls, x: tch.Tensor) -> tch.Tensor:
                if self._encoding_meth in ['sinusoid', 'trainable']:
                    if self._encoding_meth == 'sinusoid':
                        position1 = _f_emb(self._d_model, self._encoding_configs.get('max_length'),
                                          self._encoding_configs.get('base'))
                        if not hasattr(cls, 'position'):
                            cls.register_buffer('position', position1)
                    else:  # trainable
                        position1 = _f_emb(self._d_model, self._encoding_configs.get('max_length'))
                        if not hasattr(cls, 'position'):
                            cls.register_parameter('position', nn.Parameter(position1))
                return x + cls.__getattr__('position')[:x.shape[1]]  # (batch_size, seq_len, d_model)

            return _lambda_module_dict(_forward, _modules)

        elif self._encoding_meth == 'relative':
            _, _attn_config = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                          attn_init=self._attn_init, attn_forward=self._attn_forward)

            def _forward(cls: nn.ModuleDict, x: tch.Tensor, x_msk: tch.Tensor = None) -> tch.Tensor:
                # dynamic, register modules inside, pay attention on memory consumption
                batch_size, seq_len, _ = x.shape
                _max_emb_relative = self._encoding_configs.get('max_relative')
                if not hasattr(cls, _name0 := f'_relative_pos_emb_dim{seq_len}'):
                    cls.register_parameter(_name0, nn.Parameter(tch.randn(2 * self._d_model - 1, self._head_dim)))
                if not hasattr(cls, _name1 := f'_relative_pos_attn_dim{seq_len}'):
                    _attn_call, _ = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                                attn_init=self._attn_init, attn_forward=self._attn_forward)
                    cls.update({_name1: _attn_call})

                return _f_emb(self._d_model, self._num_heads, cls.__getattr__(_name1), _attn_config, batch_size,
                              seq_len, seq_len, _max_emb_relative, cls.__getattr__(_name0), x, x, x, x_msk)

            return _lambda_module_dict(_forward, _modules)

        elif self._encoding_meth == 'rotation':
            _, _attn_config = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                          attn_init=self._attn_init, attn_forward=self._attn_forward)

            def _forward(cls: nn.ModuleDict, x: tch.Tensor, x_msk: tch.Tensor = None) -> tch.Tensor:
                batch_size, seq_len, _ = x.shape
                _max_len, _theta, _start = [self._encoding_configs.get(_) for _ in ['max_length', 'theta', 'start_pos']]
                if not hasattr(cls, _name0 := f'_rotation_pos_emb_dim{seq_len}'):
                    cls.register_parameter(_name0, nn.Parameter(_f_emb(self._d_model, self._num_heads, _max_len,
                                                                       _theta)))
                if not hasattr(cls, _name1 := f'_rotation_pos_attn_dim{seq_len}'):
                    _attn_call, _ = _attentions(d_model=self._d_model, num_heads=self._num_heads,
                                                attn_init=self._attn_init, attn_forward=self._attn_forward)
                    cls.update({_name1: _attn_call})
                return _f_attn(self._d_model, self._num_heads, cls.__getattr__(_name1), _attn_config, batch_size,
                               seq_len, seq_len, cls.__getattr__(_name0), _start, x, x, x, x_msk)

            return _lambda_module_dict(_forward, _modules)

        else:
            raise NotImplementedError('the other options of positional encoding method is under developing...')

    def _encoder_chain(self):
        _modules = nn.ModuleDict({f'_encoder_{i}': self._encoder() for i in range(self._num_l[0])})

        def _forward(_, x: tch.Tensor, x_msk: tch.Tensor = None) -> tch.Tensor:
            res = self._pos_enc(self._x_vectorizer(x))
            for _, f in _modules.items():
                res = f(res, x_msk)
            return res

        return _lambda_module_dict(_forward, _modules)

    def _decoder_chain(self):
        _modules = nn.ModuleDict({f'_decoder_{i}': self._decoder() for i in range(self._num_l[1])})

        def _forward(_, x: tch.Tensor, m: tch.Tensor, x_msk: tch.Tensor = None, m_msk: tch.Tensor = None) -> tch.Tensor:
            res = self._pos_enc(self._y_vectorizer(x))
            for _, f in _modules.items():
                res = f(res, m, x_msk, m_msk)
            return res

        return _lambda_module_dict(_forward, _modules)

    def forward(self, x: tch.Tensor, m: tch.Tensor, x_msk: tch.Tensor = None, m_msk: tch.Tensor = None) -> tch.Tensor:
        mem = self.encoder(x, x_msk)
        _res = self.decoder(m, mem, x_msk, m_msk)
        return self.endmost(_res)

    @FuncTools.params_setting(train=T[Null: _Tensor], target=T[Null: _Tensor], epoch_nums=T[100: int],
                              validation=T[None: Optional[tuple[_Tensor, _Tensor]]],
                              stop_conditions=T[{'epochs': 100}: _is_valid_stop_cond],
                              loading_mode=T['local': Literal['local', 'online']],
                              **{'~unknown_tp': [tch.Tensor]})
    def solve(self, **params):
        _mod, x, y, _valid = (params.get('loading_mode'), params.get('train'), params.get('target'),
                              params.get('validation'))
        x, y = (x, None) if not isinstance(x, tuple) else x, (y, None) if not isinstance(y, tuple) else y
        x, y = (_to_tensor(x[0]), _to_tensor(x[1])), (_to_tensor(y[0]), _to_tensor(y[1]))
        _params = {k: v for k, v in params.items() if k in ['epoch_nums', 'stop_conditions', 'loading_mode']}

        if _mod == 'online':  # branch for online, need to support generator instance of x[0] and y[0]
            _train = ([v1, v2, v3, v4] for v1, v2, v3, v4 in
                      zip(x[0].unsqueeze(1), y[0].unsqueeze(1),
                          x[1].unsqueeze(1) if x[1] is not None else (None for _ in range(x[0].shape[0])),
                          y[1].unsqueeze(1) if y[1] is not None else (None for _ in range(y[0].shape[0]))))
            _target = tch.einsum('ij,ijk->ijk', y[1].float() if y[1] is not None else tch.ones_like(y[0]).float(),
                                 _as_one_hot(y[0], self._voc_size.get('out')).float()).unsqueeze(1)
            _params.update(train=_train, target=_target)

            if _valid is not None:
                x1, y1 = ((_valid[0], None) if not isinstance(_valid[0], tuple) else _valid[0],
                          (_valid[1], None) if not isinstance(_valid[1], tuple) else _valid[1])
                _train_v = ([v1, v2, v3, v4] for v1, v2, v3, v4 in
                            zip(x1[0].unsqueeze(1), y1[0].unsqueeze(1),
                                x1[1].unsqueeze(1) if x1[1] is not None else (None for _ in range(x1[0].shape[0])),
                                y1[1].unsqueeze(1) if y1[1] is not None else (None for _ in range(y1[0].shape[0]))))
                _target_v = tch.einsum('ij,ijk->ijk',
                                       y1[1].float() if y1[1] is not None else tch.ones_like(y1[0]).float(),
                                       _as_one_hot(y1[0], self._voc_size.get('out')).float()).unsqueeze(1)
                valid_ = (_train_v, _target_v)
                _params.update(validation=valid_)

        else:  # branch for local
            _train = [x[0], y[0], x[1], y[1]]
            _target = tch.einsum('ij,ijk->ijk', y[1].float() if y[1] is not None else tch.ones_like(y[0]).float(),
                                 _as_one_hot(y[0], self._voc_size.get('out')).float())
            _params.update(train=_train, target=_target)

            if _valid is not None:
                x1, y1 = ((_valid[0], None) if not isinstance(_valid[0], tuple) else _valid[0],
                          (_valid[1], None) if not isinstance(_valid[1], tuple) else _valid[1])
                _train_v = [x1[0], y1[0], x1[1], y1[1]]
                _target_v = tch.einsum('ij,ijk->ijk',
                                       y1[1].float() if y1[1] is not None else tch.ones_like(y1[0]).float(),
                                       _as_one_hot(y1[0], self._voc_size.get('out')).float())
                valid_ = (_train_v, _target_v)
                _params.update(validation=valid_)

        super().solve(**_params)

    @FuncTools.params_setting(evaluated=T[Null: _Tensor], target=T[Null: _Tensor], **{'~unknown_tp': [tch.Tensor]})
    def score(self, **params):
        x, y = params.get('evaluated'), params.get('target')
        x, y = (x, None) if not isinstance(x, tuple) else x, (y, None) if not isinstance(y, tuple) else y
        x, y = (_to_tensor(x[0]), _to_tensor(x[1])), (_to_tensor(y[0]), _to_tensor(y[1]))

        _evaluated = ([v1, v2, v3, v4] for v1, v2, v3, v4 in
                      zip(x[0].unsqueeze(1), y[0].unsqueeze(1), x[1].unsqueeze(1) if
                      x[1] is not None else (None for _ in range(x[0].shape[0])),
                      y[1].unsqueeze(1) if y[1] is not None else (None for _ in range(y[0].shape[0]))))
        _target = tch.einsum('ij,ijk->ijk', y[1].float() if y[1] is not None else tch.ones_like(y[0]).float(),
                             _as_one_hot(y[0], self._voc_size.get('out')).float()).unsqueeze(1)
        _params = {'evaluated': _evaluated, 'target': _target}
        return super().score(**_params)

    def _default_train_configs(self):
        return {
            'criterion': nn.CrossEntropyLoss(),
            'optimizer': tch.optim.Adam(self.parameters(), lr=0.001),
        }


@FuncTools.params_setting(dimension_model=T[Null: int], num_heads=T[Null: int],
                          vocabulary_size=T[{'in': 10000, 'out': 8000}: _voc_size_type],
                          embedding_func=T[{'in': None, 'out': None, 'endmost': None}: _emb_func_type],
                          encoding_meth=T['sinusoid': Literal['sinusoid', 'trainable', 'relative', 'rotation']],
                          encoding_configs=T[_encoding_config: dict], dimension_feed_forward=T[2048: int],
                          activation=T[nn.ReLU: Callable], num_layers=T[6: Union[int, tuple[int, int]]],
                          attn_init=T[None: Optional[dict]], attn_forward=T[None: Optional[dict]],
                          dropout=T[0.1: float])
@FuncTools.attach_attr(docstring=doc.transformer, info_func=False, return_tp=_Transformer)
def transformer(**params):
    return _Transformer(**params)


if __name__ == "__main__":
    pass
