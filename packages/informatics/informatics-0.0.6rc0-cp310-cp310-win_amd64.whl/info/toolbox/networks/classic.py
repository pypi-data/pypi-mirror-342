from info.toolbox.networks._frame import (tch, nn, dice, Literal, Optional, Union, Callable, FuncTools, T, Null, _Ctype,
                                          Module)
import info.docfunc as doc


_generic_conv_type = Literal['kernel_size', 'stride', 'padding', 'dilation']
_conv_kernel_type = dict[_generic_conv_type, Union[int, tuple[int, ...]]]
_norm_type = Optional[dict[Literal['eps', 'momentum', 'affine', 'track_running_state'], Union[float, bool]]]
_pool_type = Optional[dict[Literal['Max', 'FractionalMax', 'AdaptiveAvg', 'AdaptiveMax', 'Avg', 'LP', 'MaxUn'],
dict[Literal['kernel_size', 'stride', 'padding', 'dilation', 'output_size', 'output_ratio'],
Union[int, tuple[int, ...]]]]]
_valid_mpl_structure = (lambda x: isinstance(x, list) and len(x) >= 2 and all([v is None or isinstance(v, int)
                                                                               if i == 0 else isinstance(v, int) for
                                                                               i, v in enumerate(x)]))


class _FullConnected(Module):

    @FuncTools.params_setting(structure=T[Null: _valid_mpl_structure],
                              activation=T[nn.ReLU: Union[Callable, list[Callable]]],
                              bias=T[True: bool], dropout=T[None: Optional[float]], ctype_option=T['float32': _Ctype])
    def __init__(self, **params):
        super(_FullConnected, self).__init__(**params)
        self._structure, _act_func, _bias, self._ctype = (params.get('structure'), params.get('activation'),
                                                          params.get('bias'), params.get('ctype_option'))
        _dynamic = self._structure[0] is None
        _call, _args = (getattr(nn, 'LazyLinear' if _dynamic else 'Linear'),
                        [(v2,) if _dynamic else (v1, v2) for v1, v2 in zip(self._structure[:-1], self._structure[1:])])
        self._net = [_call(*_, bias=_bias, dtype=getattr(tch, self._ctype)) for _ in _args]
        _ = [setattr(self, f'_layer{i + 1}', _f) for i, _f in enumerate(self._net)]  # register modules
        self._activ = [_() for _ in _act_func] if isinstance(_act_func, list) else _act_func()  # instantiation
        self._mc = getattr(nn, 'Dropout')(_p) if (_p := params.get('dropout')) else (lambda x: x)
        self.configs = self._default_train_configs()

    def forward(self, x):
        res = None if len(self._net) > 1 else x  # support for [num1, num2]
        for i, _f in enumerate(self._net[:-1]):
            _temp = _f(x if i == 0 else res)
            res = self._activ[i](_temp) if isinstance(self._activ, list) else getattr(self, '_activ')(_temp)
        return self._mc(self._net[-1](res))

    def _default_train_configs(self):
        return {
            'criterion': nn.CrossEntropyLoss(),
            'optimizer': tch.optim.SGD(self.parameters(), lr=0.01),
        }


class _ConvComp(Module):

    @FuncTools.params_setting(out_channels=T[Null: int], activation=T[nn.ReLU: Callable],
                              in_dimensions=T[2: (lambda x: x in [1, 2, 3])],
                              conv_kernel=T[{'kernel_size': 3, 'stride': 1, 'padding': 1}: _conv_kernel_type],
                              batch_norm=T[None: _norm_type], pre_activation=T[False: bool],
                              pool=T[{'Max': {'kernel_size': 2, 'stride': 2}}: _pool_type],
                              dropout=T[None: Optional[float]], **{'~return_seq': T[False: bool]})
    def __new__(cls, **params):
        _in_dim, _pre_act, _act = (params.get('in_dimensions'), params.get('pre_activation'),
                                   params.get('activation'))
        _conv = getattr(nn, f'LazyConv{_in_dim}d')(params.get('out_channels'), **params.get('conv_kernel'))
        part1, part2 = [_conv], []
        if (_batch_args := params.get('batch_norm')) is not None:  # use batch norm
            _batch = getattr(nn, f'LazyBatchNorm{_in_dim}d')(**_batch_args)
            part2.append(_batch)
        part2.append(_act())

        part3 = [[key := [_ for _ in _pool.keys()][0], pool_args := [_ for _ in _pool.values()][0],
                 _p := 'pool' if key == 'MaxUn' else 'Pool', _attr := f'{key}{_p}{_in_dim}d',
                 getattr(nn, _attr)(**pool_args)][-1]] if (_pool := params.get('pool')) is not None else []
        part4 = [getattr(nn, f'Dropout{_in_dim}d')(_p)] if (_p := params.get('dropout')) else []

        trans_flow = part2 + part1 + part3 + part4 if _pre_act else part1 + part2 + part3 + part4
        return trans_flow if params.get('~return_seq') else nn.Sequential(*trans_flow)


class _ConvNeural(Module):

    @FuncTools.params_setting(conv_structure=T[Null: list[int]], mpl_structure=T[Null: list[int]],
                              conv_customization=T[None: Optional[list[dict]]])
    def __init__(self, **params):
        super(_ConvNeural, self).__init__()
        _conv_s, _mpl_s = params.get('conv_structure'), params.get('mpl_structure')
        self._convs = nn.ModuleList([_ConvComp(out_channels=_, **params) for _ in _conv_s] if
                                    (_conv_cus := params.get('conv_customization')) is None else
                                    [_ConvComp(out_channels=v2, **[_s := params.copy(), _s.update(**v1), _s][-1]) for
                                     v1, v2 in zip(_conv_cus, _conv_s)])
        self._mpl = _FullConnected(structure=[None]+_mpl_s, **params)  # apply dynamic mpl
        self.configs = self._default_train_configs()

    def forward(self, x):
        res = None  # just init variable, meaningless
        for i, _f in enumerate(self._convs):
            res = _f(x if i == 0 else res)
        return self._mpl(tch.flatten(res, 1, -1))

    def _default_train_configs(self):
        return {
            'criterion': nn.CrossEntropyLoss(),
            'optimizer': tch.optim.Adam(self.parameters(), lr=0.001),
        }


class _UNet(Module):

    @FuncTools.params_setting(mirrored_channels=T[[64, 128, 256, 512]: list[int]],
                              in_dimensions=T[2: (lambda x: x in [1, 2, 3])],
                              activation=T[(lambda: nn.ReLU(inplace=True)): Callable],
                              batch_norm=T[{'eps': 1e-5}: _norm_type],
                              export_channel=T[1: (lambda x: x in [1, 2, 3])])
    def __init__(self, **params):
        super(_UNet, self).__init__()
        self._in_dim, s = params.get('in_dimensions'), params.get('mirrored_channels')
        self.blocks = nn.ModuleDict({k: nn.ModuleList() for k in ['encoders', 'skip', 'decoders']})
        self._components = [self._encoder_decoder(out_channels=_, **params) for _ in (s+[s[-1]*2])]
        self._endmost = getattr(nn, f'LazyConv{self._in_dim}d')(params.get('export_channel'), kernel_size=1)
        self._register_modules()
        self.configs = self._default_train_configs()

    @FuncTools.params_setting(out_channels=T[Null: int],
                              conv_kernel=T[{'kernel_size': 3, 'stride': 1, 'padding': 1}: _conv_kernel_type],
                              pool=T[{'Max': {'kernel_size': 2, 'stride': 2}}: _pool_type])
    def _encoder_decoder(self, **params):
        _params = {**params, **{'~return_seq': True}}
        (*seq1, pool), (*seq2, _) = _ConvComp(**_params), _ConvComp(**_params)
        (*seq3, _), (*seq4, _) = _ConvComp(**_params), _ConvComp(**_params)
        enc, dec, trans = (nn.Sequential(*(seq1+seq2)), nn.Sequential(*(seq3+seq4)),
                           getattr(nn, f'LazyConvTranspose{self._in_dim}d')(params.get('out_channels'),
                                                                            **list(_params.get('pool').values())[0]))
        return enc, pool, dec, trans

    def forward(self, x):
        m = None  # just init variable, meaningless
        if x.shape.__len__() - 2 != self._in_dim:  # support the online loading mode
            x = x[tch.newaxis, ...]
        enc_series = [x := _f[0](x) if i == 0 else [_p := self._components[i-1][1], x := _f[0](_p(x)), x][-1] for
                      i, _f in enumerate(self._components)]
        dec_series = [[m := _f[-1](enc_series[-1]), m := self._remake_size(m, _d), m := tch.cat((m, _d), dim=1),
                       m := _f[2](m), m][-1] if i == 0 else [m := _f[-1](m), m := self._remake_size(m, _d),
                                                             m := tch.cat((m, _d), dim=1), m := _f[2](m), m][-1]
                      for i, (_f, _d) in enumerate(zip(self._components[:-1][::-1], enc_series[:-1][::-1]))]
        return self._endmost(dec_series[-1])

    @staticmethod
    def _remake_size(x: tch.Tensor, target: tch.Tensor):
        if x.shape != target.shape:
            x = nn.functional.interpolate(x, target.shape[2:], mode='nearest-exact')  # for precision
        return x

    def _register_modules(self):
        last = len(self._components) - 1
        for i, (enc, pool, dec, trans) in enumerate(self._components):
            if i != last:
                self.blocks.__getitem__('encoders').append(enc)
                self.blocks.__getitem__('encoders').append(pool)
                self.blocks.__getitem__('decoders').append(trans)
                self.blocks.__getitem__('decoders').append(dec)
            else:
                self.blocks.__getitem__('skip').append(enc)

    def _default_train_configs(self):
        return {
            'criterion': dice(1e-5),
            'optimizer': tch.optim.Adam(self.parameters(), lr=0.001),
        }


@FuncTools.params_setting(structure=T[Null: _valid_mpl_structure],
                          activation=T[nn.ReLU: Union[Callable, list[Callable]]],
                          bias=T[True: bool], dropout=T[None: Optional[float]], ctype_option=T['float32': _Ctype])
@FuncTools.attach_attr(docstring=doc.full_connected_neural, info_func=False, return_tp=_FullConnected)
def full_connected_neural(**params):
    return _FullConnected(**params)


@FuncTools.params_setting(conv_structure=T[Null: list[int]], mpl_structure=T[Null: list[int]],
                          activation=T[nn.ReLU: Callable], in_dimensions=T[2: (lambda x: x in [1, 2, 3])],
                          conv_kernel=T[{'kernel_size': 3, 'stride': 1, 'padding': 1}: _conv_kernel_type],
                          batch_norm=T[None: _norm_type], pre_activation=T[False: bool],
                          pool=T[{'Max': {'kernel_size': 2, 'stride': 2}}: _pool_type],
                          dropout=T[None: Optional[float]], conv_customization=T[None: Optional[list[dict]]])
@FuncTools.attach_attr(docstring=doc.convolutional_neural, info_func=False, return_tp=_ConvNeural)
def convolutional_neural(**params):
    return _ConvNeural(**params)


@FuncTools.params_setting(mirrored_channels=T[Null: list[int]], in_dimensions=T[2: (lambda x: x in [1, 2, 3])],
                          activation=T[(lambda: nn.ReLU(inplace=True)): Callable],
                          batch_norm=T[{'eps': 1e-5}: _norm_type], export_channel=T[1: int],
                          conv_kernel=T[{'kernel_size': 3, 'stride': 1, 'padding': 1}: _conv_kernel_type],
                          pool=T[{'Max': {'kernel_size': 2, 'stride': 2}}: _pool_type])
@FuncTools.attach_attr(docstring=doc.unet, info_func=False, return_tp=_UNet)
def unet(**params):
    return _UNet(**params)


if __name__ == '__main__':
    pass
