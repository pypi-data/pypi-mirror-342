from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null
# from info.basic.functions import default_param, assert_info_raiser, _as_design_mat
from info import docfunc as doc
from typing import Optional, Literal, Union, Callable
from types import GeneratorType
from itertools import tee
import numpy as np
try:
    tch = __import__('torch')
except ImportError as _:
    raise ImportError('networks requires torch installation')
nn = tch.nn
_hook = __import__('info.basic.functions', fromlist=['default_param'])
default_param, assert_info_raiser, _as_design_mat = [getattr(_hook, _) for _ in ['default_param', 'assert_info_raiser',
                                                                                 '_as_design_mat']]
Loss = getattr(nn.modules.loss, '_Loss')
Optimizer = getattr(tch.optim, 'Optimizer')
_Ctype = Literal['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
_Gen = object
_Tensor = Union[np.ndarray, tch.Tensor, _Gen]
_stop_keys = Literal['epochs', 'loss', 'accuracy']
_is_valid_stop_cond = (lambda x: (len(x) > 0 and all([k in getattr(_stop_keys, '__args__') for k in x.keys()]) and
                                  all([isinstance(v, int) and v > 0 if k == 'epochs'
                                       else v > 0 if k == 'loss' else 0 < v < 1 for k, v in x.items()])))


class InvocationError(Exception):

    pass


class Module(nn.Module):

    @FuncTools.params_setting(configs=T[None: Optional[dict]], ctype_option=T['float32': _Ctype])
    def __init__(self, **params):
        super(Module, self).__init__()  # no arguments pass on parent class
        self.configs, self._net_state, self._ctype = (default_param(params, 'configs', dict()), [],
                                                      params.get('ctype_option'))

    @FuncTools.params_setting(criterion=T[None: Optional[Union[Loss, Callable]]],
                              optimizer=T[None: Optional[Optimizer]],
                              **{'~prompt_out_interval_epoch': T[10: int], '~unknown_tp': [Loss, Optimizer]})
    def train_session(self, **params):
        print('applying training configurations...')
        _applied_keys = ['criterion', 'optimizer', '~prompt_out_interval_epoch']
        self.configs.update(__session_config={**self.configs,
                                              **{k: v if v is not None else self.configs.get(k)
                                                 for k, v in params.items() if k in _applied_keys}})
        self._net_state.append(self.training)
        self.train()
        return self

    @FuncTools.params_setting(infer_mode=T['classes': Literal['classes', 'intensities']])
    def infer_session(self, **params):
        self.configs.update(__session_config={'~infer_mode': params.get('infer_mode')})
        self._net_state.append(self.training)
        self.eval()
        return self

    @classmethod
    def _is_regression_task(cls, __target):
        if isinstance(__target, GeneratorType):
            _tmp, __target = tee(__target, 2)
            _tmp = [v for i, v in enumerate(_tmp) if i == 0][0]
        else:
            _tmp = __target
        return tch.as_tensor(_tmp).dtype == tch.float32, __target

    @FuncTools.params_setting(evaluated=T[Null: object], target=T[Null: object])
    def score(self, **params):
        (_v0_cp, _v0), (_v1_cp, _v1, _) = (tee((_ for _ in params.get('evaluated')), 2),
                                           tee((_ for _ in params.get('target')), 3))
        _valid, _c1, _c2 = (_v0, _v1), [], []  # recover variable _valid
        _is_regression, _ = self._is_regression_task([v for i, v in enumerate(_) if i < 1][0])

        with tch.no_grad():

            for _x, _y in zip(_v0_cp, _v1_cp):
                _export = (self(_x if _x.ndim > 1 else _x[..., tch.newaxis].T) if not isinstance(_x, list)
                           else self(*_x))  # list support
                _y = _y[..., tch.newaxis] if _y.ndim == 0 else _y
                if not _is_regression:
                    _, pred = tch.max(_export, -1)
                else:
                    pred = _export.data

                _c1.append(_as_design_mat(pred)[0])
                _c2.append(_as_design_mat(_y)[0])

            _pred_ref = tch.vstack(_c1)
            _y_ref = tch.vstack(_c2)

            if not _is_regression:
                _denominator = tch.prod(tch.tensor(_pred_ref.shape)) + 1
                _accuracy = tch.sum(~(_pred_ref - _y_ref).type(tch.bool)) / _denominator
            else:
                _denominator = ((_y_ref - _y_ref.mean(dim=0)) ** 2).sum(dim=0) + 1
                _accuracy = tch.mean((1 - (((_pred_ref - _y_ref) ** 2) / _denominator).sum(dim=0)).__abs__())

        return _accuracy

    def __call__(self, *args, **kwargs):
        _export = super().__call__(*args, **{k: v for k, v in kwargs.items() if not k.startswith('~')})
        if kwargs.get('~regression_caller', False):
            return _export
        if ('__session_config' in self.configs.keys() and '~infer_mode' in self.configs.get('__session_config').keys()
                and self.configs.get('__session_config').get('~infer_mode') == 'classes'):  # invoked by infer_session
            _export = _export.argmax(axis=1)
        return _export

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert_info_raiser(len(self._net_state) > 0,
                           InvocationError('activate model via methods train_session or infer_session.'))
        if len(self._net_state) == 1:
            _state = self._net_state[0]
        else:  # > 1
            *self._net_state, _state = self._net_state
        _ = self.train() if _state else self.eval()  # recovering state before session
        self.configs.update(__session_config=None)

    @staticmethod
    def _reformat_array(_obj: Union[np.ndarray, tch.Tensor, list], _is_regression: bool = None, *,
                        _to_type: _Ctype = None) -> Union[tch.Tensor, list]:
        if isinstance(_obj, list):  # support for transformer
            return _obj

        if _to_type is None:
            if _is_regression:
                _dtype = 'float32'
            else:
                _dtype = 'int64'
        else:
            _dtype = _to_type
        if isinstance(_obj, np.ndarray):
            res = tch.as_tensor(_obj.astype(getattr(np, _dtype)))
        else:
            res = _obj.type(getattr(tch, _dtype))
        return res

    @FuncTools.params_setting(train=T[Null: _Tensor], target=T[Null: _Tensor], epoch_nums=T[100: int],
                              stop_conditions=T[{'epochs': 100}: _is_valid_stop_cond],
                              validation=T[None: Optional[tuple[_Tensor, _Tensor]]],
                              loading_mode=T['online': Literal['local', 'online']], **{'~unknown_tp': [tch.Tensor]})
    def solve(self, **params):
        # Generator of [x, y, x_msk, y_msk] as each element is considered to support transformer architecture
        _conf = self.configs.get('__session_config')
        _cri, _opt, _prompt = _conf.get('criterion'), _conf.get('optimizer'), _conf.get('~prompt_out_interval_epoch')
        x, y, _valid, _mode, _stop = (params.get('train'), params.get('target'), params.get('validation'),
                                      params.get('loading_mode'), params.get('stop_conditions'))
        if _valid is None and 'accuracy' in _stop.keys():
            raise ValueError('accuracy must be calculated through given validation set.')

        _is_regression, y = self._is_regression_task(y)

        if _mode == 'local':  # type support for train & target
            x = self._reformat_array(x, None, _to_type=self._ctype)
            y = self._reformat_array(y, _is_regression)
            if _valid is not None:  # type support for validation
                _v0 = self._reformat_array(_valid[0], None, _to_type=self._ctype)
                _v1 = self._reformat_array(_valid[1], _is_regression)
                _valid = (_v0, _v1)
        else:  # online, updating all entries into generators
            x, y = ((self._reformat_array(_, None, _to_type=self._ctype) for _ in x),
                    (self._reformat_array(_, _is_regression) for _ in y))
            if _valid is not None:
                _valid = ((self._reformat_array(_, None, _to_type=self._ctype) for _ in _valid[0]),
                          (self._reformat_array(_, _is_regression) for _ in _valid[1]))

        _epoch, train_score, _accuracy, num_epoch = 1, 1e30, 0.0, _stop.get('epochs', 'Unk.')
        while all([_epoch <= v if k == 'epochs' else train_score >= v if k == 'loss' else _accuracy <= v
                   for k, v in _stop.items()]):

            self.train()
            if _mode == 'local':
                _opt.zero_grad()
                export = self(x) if not isinstance(x, list) else self(*x)  # list support transformer
                score = _cri(export, y)
                score.backward()
                _opt.step()
                train_score = score.item()
            else:  # online using generator
                (_x_cp, x), (_y_cp, y), _score = tee(x, 2), tee(y, 2), 0
                for _, (_x, _y) in enumerate(zip(_x_cp, _y_cp)):
                    _opt.zero_grad()
                    export = self(_x) if not isinstance(_x, list) else self(*_x)
                    score = _cri(export, _y)
                    score.backward()
                    _opt.step()
                    _score = score.item()
                train_score = _score

            if _valid is not None:
                self.eval()
                with tch.no_grad():
                    if _mode == 'local':
                        _export = self(_valid[0]) if not isinstance(_valid[0], list) else self(*_valid[0])
                        pred = _export.data
                        _pred, _true_y = _as_design_mat(pred), _as_design_mat(_valid[1])
                        if not _is_regression:
                            _, _pred = tch.max(_pred, -1)
                            _accuracy = sum([v1 == v2 for v1, v2 in zip(pred, _valid[1])]) / len(_valid[1])
                        else:
                            _denominator = ((_true_y - _true_y.mean(dim=0)) ** 2).sum(dim=0) + 1
                            _accuracy = tch.mean((1 - (((_pred - _true_y) ** 2) / _denominator).sum(dim=0)).__abs__())
                    else:  # online using generator
                        (_v0_cp, _v0), (_v1_cp, _v1) = tee(_valid[0], 2), tee(_valid[1], 2)
                        _valid, _c1, _c2 = (_v0, _v1), [], []  # recover variable _valid
                        for _x, _y in zip(_v0_cp, _v1_cp):
                            _export = (self(_x if _x.ndim > 1 else _x[..., tch.newaxis].T) if not isinstance(_x, list)
                                       else self(*_x))  # list support
                            _y = _y[..., tch.newaxis] if _y.ndim == 0 else _y
                            if not _is_regression:
                                _, pred = tch.max(_export, -1)
                            else:
                                pred = _export.data

                            _c1.append(_as_design_mat(pred)[0])
                            _c2.append(_as_design_mat(_y)[0])

                        _pred_ref = tch.vstack(_c1)
                        _y_ref = tch.vstack(_c2)

                        if not _is_regression:
                            _denominator = tch.prod(tch.tensor(_pred_ref.shape)) + 1
                            _accuracy = tch.sum(~(_pred_ref - _y_ref).type(tch.bool)) / _denominator
                        else:
                            _denominator = ((_y_ref - _y_ref.mean(dim=0)) ** 2).sum(dim=0) + 1
                            _accuracy = tch.mean((1 - (((_pred_ref -
                                                         _y_ref) ** 2) / _denominator).sum(dim=0)).__abs__())

            if _prompt > 0:
                if _epoch % _prompt == 0:
                    _msg = f'Epoch [{_epoch}/{num_epoch}], Loss: {train_score:.4f}'
                    if _valid is not None:
                        _msg = _msg + f', Accuracy: {_accuracy:.4f}'
                    print(_msg)

            _epoch += 1


def _dice(x, y, e):
    if y.shape != x.shape:  # support online loading mode
        y = y[tch.newaxis, ...]
    x = tch.sigmoid(x)
    _agg_dim = tuple(_ for _ in range(len(x.shape)) if _ not in [0, 1])
    intersection, denominator = (x * y).sum(dim=_agg_dim), x.sum(dim=_agg_dim) + y.sum(dim=_agg_dim) + e
    numerator = 2 * intersection + e
    return 1 - (numerator / denominator).mean()


dice = (lambda smooth: (lambda x, y: _dice(x, y, e=smooth)))


doc.redoc(Module, doc.Module)


if __name__ == '__main__':
    pass
