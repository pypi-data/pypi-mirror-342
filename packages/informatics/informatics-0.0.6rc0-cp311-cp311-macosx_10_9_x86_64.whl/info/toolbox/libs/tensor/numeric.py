# static import:
from info.basic.typehint import Numeric, T, Null
from info.basic.decorators import FuncTools
from info.basic.core import TrialDict
from info.basic.functions import assert_info_raiser, default_param
import info.docfunc as doc
from typing import Sequence, Optional, Union, Literal, Iterable, Callable
from warnings import warn
from tensorly import (cp_to_tensor, tucker_to_tensor, tt_to_tensor, tr_to_tensor, validate_cp_rank,
                      validate_tucker_rank, validate_tt_rank)
from tensorly.decomposition import parafac, tucker, tensor_train, tensor_ring
from scipy.interpolate import interp1d
import numpy
# init for dynamic import:
import numpy as _np
from scipy.ndimage import correlate as _correlate
from scipy.ndimage import convolve as _convolve
from scipy.ndimage import binary_erosion as _binary_erosion
from scipy.ndimage import generic_filter as _generic_filter
from numpy import ndarray as np_ndarray
try:
    cp_ndarray = __import__('cupy', fromlist=['ndarray']).ndarray
except ImportError as _:
    cp_ndarray = np_ndarray
bsc = __import__('info.toolbox.libs._basic', fromlist=['_basic'])
fun = __import__('info.basic.functions', fromlist=['_get_gs_thre'])
KernelGen = getattr(bsc, 'KernelGen')
averaging_kernel = getattr(bsc, 'averaging_kernel')
gaussian_kernel = getattr(bsc, 'gaussian_kernel')
gabor_kernel = getattr(bsc, 'gabor_kernel')
laplacian_of_gaussian_kernel = getattr(bsc, 'laplacian_of_gaussian_kernel')
LOG_2PI = getattr(bsc, 'LOG_2PI')
PI2 = getattr(bsc, 'PI2')
_basic_config = getattr(bsc, 'config')
_get_gs_thre = getattr(fun, '_get_gs_thre')
_margin = getattr(fun, '_margin')
_pairwise_to_center = getattr(fun, '_pairwise_to_center')
_diff_op = getattr(fun, '_diff_op')
_gs_bin = getattr(fun, '_gs_bin')
_pairwise_gs_kernel = getattr(fun, '_pairwise_gs_kernel')
_make_orthogonal_cursor = getattr(fun, '_make_orthogonal_cursor')
_ternarization = getattr(fun, '_ternarization')
ext_rank1 = (lambda x, b, meth: [sp := x.shape, tmp1 := numpy.array([_.ravel() for _ in
                                                                     numpy.split(x, sp[1], axis=1)]).T,
                                 org_x := numpy.array([_ for _ in range(sp[1])]),
                                 new_x := numpy.linspace(0, sp[1]-1, b),
                                 numpy.concatenate([_.reshape((sp[0], 1, sp[2])) for _ in
                                                    numpy.array([interp1d(org_x, _, kind=meth)(new_x)
                                                                 for _ in tmp1]).T],
                                                   axis=1)][-1])


np, ndarray, correlate, convolve, binary_erosion, generic_filter = (_np, np_ndarray, _correlate, _convolve,
                                                                    _binary_erosion, _generic_filter)
dual_ndarray = Union[np_ndarray, cp_ndarray]


class _Config:

    verbosity = False

    def __init__(self):
        global np, ndarray, correlate, convolve, binary_erosion, generic_filter
        import numpy as np
        from numpy import ndarray
        from scipy.ndimage import correlate, convolve, binary_erosion, generic_filter
        _basic_config.reset(device='cpu')
        self.device_ = 'cpu'
        print(np, ndarray, correlate, convolve, binary_erosion, generic_filter,
              _basic_config.device_) if self.verbosity else ...

    @FuncTools.params_setting(device=T['cpu': Literal['cpu', 'gpu']])
    def reset(self, **params):
        self.device_ = params.get('device')
        global np, ndarray, correlate, convolve, binary_erosion, generic_filter
        if self.device_ == 'cpu':
            import numpy as np
            from numpy import ndarray
            from scipy.ndimage import correlate, convolve, binary_erosion, generic_filter
            _basic_config.reset(device='cpu')
            print(np, ndarray, correlate, convolve, binary_erosion, generic_filter,
                  _basic_config.device_) if self.verbosity else ...
        if self.device_ == 'gpu':
            try:
                np = __import__('cupy')
                ndarray = __import__('cupy', fromlist=['ndarray']).ndarray
                correlate = __import__('cupyx.scipy.ndimage', fromlist=['correlate']).correlate
                convolve = __import__('cupyx.scipy.ndimage', fromlist=['convolve']).convolve
                binary_erosion = __import__('cupyx.scipy.ndimage', fromlist=['convolve']).binary_erosion
                generic_filter = __import__('cupyx.scipy.ndimage', fromlist=['generic_filter']).generic_filter
                _basic_config.reset(device='gpu')
            except ImportError as _:
                warn('Cuda or Cupy is not available, reset default device as cpu...')
                self.reset(device='cpu')
            print(np, ndarray, correlate, convolve, binary_erosion, generic_filter,
                  _basic_config.device_) if self.verbosity else ...


config = _Config()


@FuncTools.params_setting(data=T[Null: dual_ndarray])
@FuncTools.attach_attr(docstring=doc.standardization, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def standardization(**params):
    dt: ndarray = params.get('data')
    return (dt - dt.mean()) / dt.std()


@FuncTools.params_setting(data=T[Null: dual_ndarray])
@FuncTools.attach_attr(docstring=doc.normalization, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def normalization(**params):
    dt: ndarray = params.get('data')
    return (dt - np.min(dt)) / (np.max(dt) - np.min(dt))


@FuncTools.params_setting(data=T[Null: dual_ndarray], moment_order=T[1: int], moment_center=T[None: Optional[Numeric]],
                          moment_axis=T[None: Optional[Union[int, tuple[int, ...]]]], moment_rescale=T[False: bool])
@FuncTools.attach_attr(docstring=doc.under_editing, info_func=True, entry_tp=dual_ndarray,
                       return_tp=Union[dual_ndarray, Numeric])
def moment(**params):
    meta, k, c, axis, rescale = (params.get('data'), params.get('moment_order'), params.get('moment_center'),
                                 params.get('moment_axis'), params.get('moment_rescale'))
    meta, axis = (meta, tuple(_ for _ in range(meta.ndim))) if axis is None else (meta, axis)
    meta = meta if c is None else meta - c
    m = (np.sum(meta, axis=axis)**k).astype(float)  # to float for debugging np.int32/np.float64 return
    return np.multiply(m, np.reciprocal(np.std(meta, axis=axis)**k)) if rescale else m


@FuncTools.params_setting(data=T[Null: dual_ndarray], clip=T[Null: tuple[Numeric, Numeric]])
@FuncTools.attach_attr(docstring=doc.clipper, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def clipper(**params):
    dt: ndarray = params.get('data')
    clip: list = params.get('clip')
    return dt.clip(min=clip[0], max=clip[1])


@FuncTools.params_setting(data=T[Null: dual_ndarray], crop_range=T[Null: list[tuple[Numeric, ...]]])
@FuncTools.attach_attr(docstring=doc.cropper, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def cropper(**params):
    dt: ndarray = params.get('data')
    crop_range: list = params.get('crop_range')
    shape, dim = dt.shape, dt.ndim

    # type check for crop_range
    try:
        assert len(crop_range) == 2
        assert len(crop_range[0]) == len(crop_range[1])
        assert len(crop_range[0]) == dim
        for _s, _e in zip(crop_range[0], crop_range[1]):
            assert _s <= _e
    except AssertionError as _:
        raise TypeError("'crop_range' should be form of [start_idx_tuple, end_idx_tuple]")

    # determine crop mode
    absolute = True
    if np.any(np.array(list(map(lambda x: isinstance(x, float), crop_range[0] + crop_range[1])))):
        absolute = False

    # cropping steps
    for _ in range(len(crop_range[0])):
        start, end, length = crop_range[0][_], crop_range[1][_], shape[_]
        if not absolute:
            start, end = round(start * length), round(end * length)
        _slices = np.split(dt, length, axis=_)
        dt = np.concatenate(_slices[start: end], axis=_)

    return dt


@FuncTools.params_setting(data=T[Null: dual_ndarray], new_size=T[Null: tuple[int, ...]],
                          decomp_method=T['cp': Literal['cp', 'tucker', 'tt', 'tr']],
                          decomp_rank=T[None: Optional[Union[int, tuple[int, ...]]]],
                          interp_method=T['linear': Literal['linear', 'nearest', 'nearest-up', 'zero', 'slinear',
                          'quadratic', 'cubic', 'previous', 'next']])
@FuncTools.attach_attr(docstring=doc.resize, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def resize(**params):
    data, new_size, method, decomp, rk = (params.get('data').astype(float), params.get('new_size'),
                                          params.get('interp_method'), params.get('decomp_method'),
                                          params.get('decomp_rank'))
    if decomp in ['tucker', 'tt'] and data.ndim < 2:
        warn("tucker or tensor train decomposition cannot be applied on tensor with rank 1, try 'cp'...")
        decomp, rk = 'cp', rk[0] if isinstance(rk, tuple) else rk
    if decomp == 'tr' and data.ndim < 3:
        warn("tensor ring decomposition cannot be applied on tensor with rank no greater than 2, try 'cp'...")
        decomp, rk = 'cp', rk[0] if isinstance(rk, tuple) else rk

    if hasattr(data, 'get'):  # in cpu, interp1d is not supported in cupy
        data = data.get()

    if decomp in ['cp', 'tucker']:
        rk = rk if rk is not None else validate_cp_rank(data.shape) if decomp == 'cp' else (
            validate_tucker_rank(data.shape))
        core, mats = parafac(data, rk) if decomp == 'cp' else tucker(data, rk)
        org_x = [numpy.array([_ for _ in range(dim)]) for dim in data.shape]
        new_x = [numpy.linspace(0, org_x[_][-1], new_size[_]) for _ in range(len(new_size))]
        n_mats = tuple(numpy.array([interp1d(org_x[nd], _, kind=method)(new_x[nd]) for _ in mats[nd].T]).T
                       for nd in range(len(mats)))
        res = np.array(cp_to_tensor((core, n_mats))) if decomp == 'cp' else np.array(tucker_to_tensor((core, n_mats)))
    else:
        rk = rk if rk is not None else validate_tt_rank(data.shape) if decomp == 'tt' else (
            tuple(1 for _ in range(data.ndim + 1)))  # bug in validate_tr_rank
        factors = tensor_train(data, rk) if decomp == 'tt' else tensor_ring(data, rk)
        new_factors = [ext_rank1(v1, v2, method) for v1, v2 in zip(factors, new_size)]
        res = np.array(tt_to_tensor(new_factors)) if decomp == 'tt' else np.array(tr_to_tensor(new_factors))
    return res


def _pre_generic_map(x: ndarray, k: ndarray, mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                     cval: float, origin: Union[int, Sequence]) -> tuple[ndarray, tuple[int, ...]]:
    """intrinsic iterator of scipy"""
    res = []

    def run(blk):
        res.append(blk)
        return 0

    # from scipy.ndimage import generic_filter as _iter  # scipy.ndimage.generic_filter as default iterator
    # if hasattr(x, 'get'):  # implicit conversion, branch for cupy.ndarray
    #     x = x.get()
    # _iter(x, run, k.shape, mode=mode, cval=cval, origin=origin)
    generic_filter(x, run, k.shape, mode=mode, cval=cval, origin=origin)
    return np.array(res), x.shape


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.averaging_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def averaging_filter(**params):
    k: KernelGen = averaging_kernel(k_shape=params.get('k_shape'))
    return correlate(params.get('data'), k, output=k.dtype, mode=params.get('k_mode'), cval=params.get('k_cval'),
                     origin=params.get('k_origin'))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]], k_rank=T[Null: Numeric],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.rank_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def rank_filter(**params):
    m1, m2 = _pre_generic_map(params.get('data'), np.ones(params.get('k_shape')), params.get('k_mode'),
                              params.get('k_cval'), params.get('k_origin'))

    ptr, size = params.get('k_rank'), m1.shape[1]
    if isinstance(ptr, int):
        if ptr < 0:
            ptr += size
        ptr = ptr/(size-1)
    assert_info_raiser(-1 < ptr <= 1, TypeError(f'{ptr} must be int, or float from 0. to 1.'))
    ptr = ptr + 1 if ptr < 0 else ptr  # support for minus assign
    return np.quantile(m1, [ptr], axis=1)[0].reshape(m2)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.minimum_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def minimum_filter(**params):
    m1, m2 = _pre_generic_map(params.get('data'), np.ones(params.get('k_shape')), params.get('k_mode'),
                              params.get('k_cval'), params.get('k_origin'))
    return np.min(m1, axis=1).reshape(m2)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.maximum_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def maximum_filter(**params):
    m1, m2 = _pre_generic_map(params.get('data'), np.ones(params.get('k_shape')), params.get('k_mode'),
                              params.get('k_cval'), params.get('k_origin'))
    return np.max(m1, axis=1).reshape(m2)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.mean_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def mean_filter(**params):
    m1, m2 = _pre_generic_map(params.get('data'), np.ones(params.get('k_shape')), params.get('k_mode'),
                              params.get('k_cval'), params.get('k_origin'))
    return np.mean(m1, axis=1).reshape(m2)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.median_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def median_filter(**params):
    m1, m2 = _pre_generic_map(params.get('data'), np.ones(params.get('k_shape')), params.get('k_mode'),
                              params.get('k_cval'), params.get('k_origin'))
    return np.median(m1, axis=1).reshape(m2)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]],
                          k_mu=T[None: Optional[ndarray]], k_sigma=T[None: Optional[ndarray]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.gaussian_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def gaussian_filter(**params):
    shape = params.get('k_shape')
    mu, sigma = (default_param(params, 'k_mu', np.zeros_like(np.array(shape))),
                 default_param(params, 'k_sigma', np.diag(shape)))
    k: KernelGen = gaussian_kernel(k_shape=params.get('k_shape'), k_mu=mu, k_sigma=sigma)
    return correlate(params.get('data'), k, mode=params.get('k_mode'), cval=params.get('k_cval'),
                     origin=params.get('k_origin'), output=k.dtype)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]], k_rescale=T[1: Numeric],
                          k_orientation=T[None: Optional[list[Numeric]]], k_wavelength=T[PI2: Numeric],
                          k_phase=T[0: Numeric], k_mode=T['reflect': Literal['reflect', 'constant', 'nearest',
                          'mirror', 'wrap']], k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.gabor_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def gabor_filter(**params):
    shape = params.get('k_shape')
    direction = default_param(params, 'k_orientation', [1 for _ in range(len(shape))])
    assert_info_raiser(len(shape) == len(direction), ValueError('k_orientation must be identical dimensions as data'))
    k: KernelGen = gabor_kernel(k_shape=shape, k_rescale=params.get('k_rescale'), k_orientation=direction,
                                k_wavelength=params.get('k_wavelength'), k_phase=params.get('k_phase'))
    return convolve(params.get('data'), k, mode=params.get('k_mode'), cval=params.get('k_cval'),
                    origin=params.get('k_origin'), output=k.dtype)  # no symmetry guaranteed, use convolve


def _rescale(x: ndarray, axis: int) -> ndarray:
    """element-wise rescale divided by sum along assigned axis"""
    margin, _slices = np.reciprocal(x.sum(axis=axis)+1e-40), np.split(x, x.shape[axis], axis)
    return np.stack([np.multiply(item.sum(axis=axis), margin) for item in _slices], axis=axis)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[Null: tuple[int, ...]],
                          sigma_d=T[None: Optional[ndarray]], sigma_r=T[None: Optional[Numeric]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.bilateral_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def bilateral_filter(**params):
    _params, shape = TrialDict(**params), params.get('k_shape')
    _params.update(shape=shape)
    _, tensor = KernelGen(**_params), _params.get('data')
    sigma_d = default_param(params, 'sigma_d', np.diag(np.array(_.shape)))
    mvn_k, other_info = gaussian_kernel(**_params.trial(**{'~other_info': True, 'k_mu': _.rela_anchor,
                                                           'k_sigma': sigma_d}))

    mvn_item = np.log(np.ravel(mvn_k)) + 0.5 * (np.log(np.linalg.det(other_info[0])) + other_info[1] * LOG_2PI)
    blocks, org_shape = _pre_generic_map(tensor, mvn_k, mode=_params.get('k_mode'), cval=_params.get('k_cval'),
                                         origin=_params.get('k_origin'))
    _kernels = (blocks.T - blocks.T[_.anchor_id]).T
    if params.get('sigma_r') is not None:
        sigma_r = params.get('sigma_r')
        _kernels = np.square(_kernels) * (-0.5) * np.reciprocal(np.square(sigma_r)+1e-40) + mvn_item
    else:  # local adaptive sigma_r
        _ = np.array([(-0.5) * (1 / (np.var(_kernels, axis=1) + 1e-40))])
        _kernels = np.square(_kernels) * np.repeat(_, _kernels.shape[1], axis=0).T + mvn_item
    kernels = _rescale(np.exp(_kernels), axis=1)
    return np.multiply(blocks, kernels).sum(axis=1).reshape(org_shape)


def _kernels_maker(x: list[KernelGen], axis: int, sub: Union[int, ndarray, KernelGen] = 1) -> ndarray:
    len_ = len(x)
    if len_ == 1:
        _res = [np.zeros_like(x[0])]
        _res[0][tuple(x[0].anchor)] = 1
    else:
        _res = [np.zeros_like(item) for item in x]
        if isinstance(sub, int):
            sub = np.ones_like(_res[-1]) * sub
        _res[0] -= sub
        _res[-1] += sub
    _res = np.concatenate(_res, axis=axis)
    return _res / _res.__abs__().sum()


def _detector_kernels(x: KernelGen, subs: Union[int, list[Union[ndarray, KernelGen]]] = 1) -> list[ndarray]:
    _org, shape = np.zeros_like(x), x.shape
    _slices = [np.split(_org, shape[_], _) for _ in range(x.ndim)]  # nested list
    if isinstance(subs, int):
        return [_kernels_maker(_slices[_], _, subs) for _ in range(x.ndim)]
    else:
        return [_kernels_maker(_slices[_], _, subs[_]) for _ in range(x.ndim)]


def _prewitt(**params):
    tensor: ndarray = params.get('data').astype(float)
    org_domain = [np.amin(tensor), np.amax(tensor)]
    k_shape = default_param(params, 'k_shape', tuple(3 for _ in range(tensor.ndim)))
    k_base: KernelGen = KernelGen(shape=k_shape, fill=0)
    prewitt_ks = _detector_kernels(k_base)
    tensor_diffs = [correlate(tensor, k, output=float, mode=params.get('k_mode'), cval=params.get('k_cval'),
                              origin=params.get('k_origin')) for k in prewitt_ks]

    _res = np.linalg.norm(np.array(tensor_diffs), ord=2, axis=0).clip(org_domain[0], org_domain[1])

    if params.get('~as_filter', False):  # branch for filter, bool
        return _res

    if coef := params.get('~as_sharpen', False):  # branch for sharpen, Numeric
        prewitt_ks_abs = [np.abs(k) for k in prewitt_ks]
        tensor_refs = [correlate(tensor, k, mode=params.get('k_mode'), cval=params.get('k_cval'),
                                 origin=params.get('k_origin')) for k in prewitt_ks_abs]
        augments = [np.multiply(np.sign(tensor - ref), diff) for ref, diff in zip(tensor_refs, tensor_diffs)]

        tensor = tensor.astype(float)
        for _ in augments:
            tensor += coef * _  # augment for edge
        return tensor.clip(org_domain[0], org_domain[1])

    if thre := params.get('~as_detector', False):  # branch for detector, Numeric
        res = np.zeros_like(_res)
        if 0 < thre < 1:
            thre = np.quantile(_res, [thre])[0]
        res[np.where(_res >= thre)] = 1
        return res.astype(bool)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.prewitt_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def prewitt_filter(**params):
    _params: TrialDict = TrialDict(**params)
    return _prewitt(**_params.trial(**{'~as_filter': True, '~as_detector': False, '~as_sharpen': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]],
                          prewitt_limen=T[0.9: Numeric])
@FuncTools.attach_attr(docstring=doc.prewitt_detector, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def prewitt_detector(**params):
    _params: TrialDict = TrialDict(**params)
    return _prewitt(**_params.trial(**{'~as_detector': params.get('prewitt_limen'), '~as_filter': False,
                                       '~as_sharpen': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], sharp_alpha=T[1: Numeric])
@FuncTools.attach_attr(docstring=doc.prewitt_sharpen, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def prewitt_sharpen(**params):
    _params: TrialDict = TrialDict(**params)
    return _prewitt(**_params.trial(**{'~as_sharpen': params.get('sharp_alpha', 1), '~as_filter': False,
                                       '~as_detector': False}))


def _sobel(**params):
    tensor: ndarray = params.get('data')
    g_base = gaussian_kernel(k_shape=default_param(params, 'k_shape', tuple(3 for _ in range(tensor.ndim))))

    if params.get('~applied_gaussian_kernel', False):  # branch for canny-derived, bool
        tensor: ndarray = correlate(tensor, g_base, mode=params.get('k_mode', 'reflect'),
                                    cval=params.get('k_cval', 0.0), origin=params.get('k_origin', 0))

    org_domain = [np.amin(tensor), np.amax(tensor)]
    subs = [g_base.sum(axis=_, keepdims=True) for _ in range(g_base.ndim)]
    kernels = _detector_kernels(g_base, subs)
    tensor_diffs = [correlate(tensor, k, output=float, mode=params.get('k_mode', 'reflect'),
                              cval=params.get('k_cval', 0.0), origin=params.get('k_origin', 0)) for k in kernels]

    _res = np.linalg.norm(np.array(tensor_diffs), ord=2, axis=0).clip(org_domain[0], org_domain[1])

    if params.get('~as_filter', False):  # branch for filter, bool
        return _res

    if coef := params.get('~as_sharpen', False):  # branch for sharpen, Numeric
        kernels_abs = [np.abs(k) for k in kernels]
        tensor_refs = [correlate(tensor, k, output=float, mode=params.get('k_mode', 'reflect'),
                                 cval=params.get('k_cval', 0.0), origin=params.get('k_origin', 0)) for k in kernels_abs]
        augments = [np.multiply(np.sign(tensor - ref), diff) for ref, diff in zip(tensor_refs, tensor_diffs)]

        tensor = tensor.astype(float)
        for _ in augments:
            tensor += coef * _  # augment for edge
        return tensor.clip(org_domain[0], org_domain[1])

    if thre := params.get('~as_detector', False):  # branch for detector, Numeric
        res = np.zeros_like(_res)
        if 0 < thre < 1:
            thre = np.quantile(_res, [thre])[0]
        res[np.where(_res >= thre)] = 1
        return res.astype(bool)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.sobel_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def sobel_filter(**params):
    _params: TrialDict = TrialDict(**params)
    return _sobel(**_params.trial(**{'~as_filter': True, '~as_detector': False, '~as_sharpen': False,
                                     '~applied_gaussian_kernel': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], sobel_limen=T[0.9: Numeric])
@FuncTools.attach_attr(docstring=doc.sobel_detector, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def sobel_detector(**params):
    _params: TrialDict = TrialDict(**params)
    return _sobel(**_params.trial(**{'~as_detector': params.get('sobel_limen'), '~as_filter': False,
                                     '~as_sharpen': False, '~applied_gaussian_kernel': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], sharp_alpha=T[1: Numeric])
@FuncTools.attach_attr(docstring=doc.sobel_sharpen, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def sobel_sharpen(**params):
    _params: TrialDict = TrialDict(**params)
    return _sobel(**_params.trial(**{'~as_sharpen': params.get('sharp_alpha'), '~as_filter': False,
                                     '~as_detector': False, '~applied_gaussian_kernel': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.canny_filter, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def canny_filter(**params):
    _params: TrialDict = TrialDict(**params)
    return _sobel(**_params.trial(**{'~as_filter': True, '~as_detector': False, '~as_sharpen': False,
                                     '~applied_gaussian_kernel': True}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], canny_limen=T[0.9: Numeric])
@FuncTools.attach_attr(docstring=doc.sobel_detector, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def canny_detector(**params):
    _params: TrialDict = TrialDict(**params)
    return _sobel(**_params.trial(**{'~as_detector': params.get('sobel_limen', params.get('canny_limen')),
                                     '~as_filter': False, '~as_sharpen': False, '~applied_gaussian_kernel': True}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], sharp_alpha=T[1: Numeric])
@FuncTools.attach_attr(docstring=doc.sobel_sharpen, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def canny_sharpen(**params):
    _params: TrialDict = TrialDict(**params)
    return _sobel(**_params.trial(**{'~as_sharpen': params.get('sharp_alpha'), '~as_filter': False,
                                     '~as_detector': False, '~applied_gaussian_kernel': True}))


def _laplacian_of_gaussian(**params) -> ndarray:
    tensor = params.get('data')
    org_domain = [np.amin(tensor), np.amax(tensor)]
    _params: TrialDict = TrialDict(**params)
    k_shape = default_param(params, 'k_shape', tuple(3 for _ in range(tensor.ndim)))
    log_base: ndarray = laplacian_of_gaussian_kernel(**_params.trial(**{'k_shape': k_shape}))
    log_base = log_base - log_base.mean()
    log_base = log_base/log_base.__abs__().sum()

    if params.get('~as_filter', False):  # branch for filter, bool
        return correlate(tensor, log_base, output=log_base.dtype, mode=_params.get('k_mode', 'reflect'),
                         cval=_params.get('k_cval', 0.0), origin=_params.get('k_origin', 0))

    if coef := params.get('~as_sharpen', False):  # branch for sharpen, Numeric
        log_base = log_base * (-2)
        aug = correlate(tensor, log_base, output=log_base.dtype, mode=_params.get('k_mode', 'reflect'),
                        cval=_params.get('k_cval', 0.0), origin=_params.get('k_origin', 0))
        aug = coef * aug
        res = tensor + aug
        return res.clip(org_domain[0], org_domain[1])

    if thre := params.get('~as_detector', False):  # branch for detector, Numeric
        _res = correlate(tensor, log_base, output=log_base.dtype, mode=_params.get('k_mode', 'reflect'),
                         cval=_params.get('k_cval', 0.0),
                         origin=_params.get('k_origin', 0)).clip(org_domain[0], org_domain[1])
        res = np.zeros_like(_res)
        if 0 < thre < 1:
            thre = np.quantile(_res, [thre])[0]
        res[np.where(_res >= thre)] = 1
        return res.astype(bool)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.laplacian_of_gaussian_filter, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def laplacian_of_gaussian_filter(**params):
    _params: TrialDict = TrialDict(**params)
    return _laplacian_of_gaussian(**_params.trial(**{'~as_filter': True, '~as_detector': False, '~as_sharpen': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], log_limen=T[0.9: Numeric])
@FuncTools.attach_attr(docstring=doc.laplacian_of_gaussian_detector, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def laplacian_of_gaussian_detector(**params):
    _params: TrialDict = TrialDict(**params)
    return _laplacian_of_gaussian(**_params.trial(**{'~as_detector': params.get('log_limen'), '~as_filter': False,
                                                     '~as_sharpen': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], sharp_alpha=T[1: Numeric])
@FuncTools.attach_attr(docstring=doc.sobel_sharpen, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def laplacian_of_gaussian_sharpen(**params):
    _params: TrialDict = TrialDict(**params)
    return _laplacian_of_gaussian(**_params.trial(**{'~as_sharpen': params.get('sharp_alpha'), '~as_filter': False,
                                                     '~as_detector': False}))


def _dog(x, k_shape, sigma_seq, k_mode, k_cval, k_origin):
    ks = [gaussian_kernel(k_shape=k_shape, k_sigma=_*np.eye(x.ndim)) for _ in sigma_seq]
    return np.diff([correlate(x, k, mode=k_mode, cval=k_cval, origin=k_origin, output=k.dtype) for k in ks], axis=0)


def _difference_of_gaussian(**params):
    tensor = params.get('data')
    k_shape = default_param(params, 'k_shape', tuple(3 for _ in range(tensor.ndim)))
    sigma_seq = [1, default_param(params, 'sigma_ratio', 1.75)]
    org_domain = [np.amin(tensor), np.amax(tensor)]
    _res = _dog(params.get('data'), k_shape, sigma_seq, params.get('k_mode'), params.get('k_cval'),
                params.get('k_origin'))[0] * (-0.5)
    if params.get('~as_filter', False):  # branch for filter, bool
        return _res
    if coef := params.get('~as_sharpen', False):  # branch for sharpen, Numeric
        aug = coef * _res
        res = tensor + aug
        return res.clip(org_domain[0], org_domain[1])
    if thre := params.get('~as_detector', False):  # branch for detector, Numeric
        _res = _res.clip(org_domain[0], org_domain[1])
        res = np.zeros_like(_res)
        if 0 < thre < 1:
            thre = np.quantile(_res, [thre])[0]
        res[np.where(_res >= thre)] = 1
        return res.astype(bool)


@FuncTools.params_setting(data=T[Null: dual_ndarray], sigma_ratio=T[1.6: Numeric],
                          k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]])
@FuncTools.attach_attr(docstring=doc.difference_of_gaussian_filter, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def difference_of_gaussian_filter(**params):
    _params: TrialDict = TrialDict(**params)
    return _difference_of_gaussian(**_params.trial(**{'~as_filter': True, '~as_detector': False, '~as_sharpen': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], sigma_ratio=T[1.6: Numeric],
                          k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], dog_limen=T[0.9: Numeric])
@FuncTools.attach_attr(docstring=doc.difference_of_gaussian_detector, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def difference_of_gaussian_detector(**params):
    _params: TrialDict = TrialDict(**params)
    return _difference_of_gaussian(**_params.trial(**{'~as_detector': params.get('dog_limen'), '~as_filter': False,
                                                      '~as_sharpen': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], sigma_ratio=T[1.6: Numeric],
                          k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], k_origin=T[0: Union[int, Sequence[int]]], sharp_alpha=T[1: Numeric])
@FuncTools.attach_attr(docstring=doc.difference_of_gaussian_sharpen, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def difference_of_gaussian_sharpen(**params):
    _params: TrialDict = TrialDict(**params)
    return _difference_of_gaussian(**_params.trial(**{'~as_sharpen': params.get('sharp_alpha'), '~as_filter': False,
                                                      '~as_detector': False}))


def _hessian(**params):
    tensor: ndarray = params.get('data').astype(float)
    _sp = params.get('in_spacing')
    k_shape = default_param(params, 'k_shape', tuple(3 for _ in range(tensor.ndim)))
    assert_info_raiser(all([_ >= 3 for _ in k_shape]),
                       ValueError('each dimension of differential operator should be no less than 3'))
    _sp = _sp if hasattr(_sp, '__iter__') else tuple(_sp for _ in range(len(k_shape)))
    frac = [0.5/(v1*(v2-1)) for v1, v2 in zip(_sp, k_shape)]
    k_base: KernelGen = KernelGen(shape=k_shape, fill=0)
    diff_ks = [_margin(v1, i)*v2 for i, (v1, v2) in enumerate(zip(_detector_kernels(k_base), frac))]
    _gradient = (lambda x, ks: [correlate(x, k, output=float, mode=params.get('k_mode'), cval=params.get('k_cval'),
                                          origin=0) for k in ks])
    diff1 = _gradient(tensor, diff_ks)
    hessian_ = np.array([np.linalg.det(_) for _ in np.array([[_.ravel() for _ in _gradient(_, diff_ks)]
                         for _ in diff1]).transpose((2, 0, 1))]).reshape(tensor.shape)

    if params.get('~as_response'):  # branch for hessian determinant response
        return hessian_

    scales = np.array([_ ** 2 for _ in diff1 + [np.ones_like(tensor)]]).sum(axis=0) ** 2
    curvature = np.multiply(hessian_, np.reciprocal(scales))

    if params.get('~as_curvature'):    # branch for hessian curvature, bool
        return curvature

    if thre := params.get('~as_detector'):  # branch for detector, Numeric
        res = np.zeros_like(curvature)
        _s = np.sort(curvature[curvature != 0].ravel())
        thre = _s[round(len(_s)*thre)]  # 0 < thre < 1
        res[np.where(curvature >= thre)] = 1
        return res.astype(bool)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], in_spacing=T[1: Union[Numeric, tuple[Numeric, ...]]])
@FuncTools.attach_attr(docstring=doc.hessian_determinant_response, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def hessian_determinant_response(**params):
    _params: TrialDict = TrialDict(**params)
    return _hessian(**_params.trial(**{'~as_curvature': False, '~as_detector': False, '~as_response': True}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], in_spacing=T[1: Union[Numeric, tuple[Numeric, ...]]])
@FuncTools.attach_attr(docstring=doc.hessian_curvature_detector, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def hessian_curvature_response(**params):
    _params: TrialDict = TrialDict(**params)
    return _hessian(**_params.trial(**{'~as_curvature': True, '~as_detector': False, '~as_response': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0.0: Numeric], in_spacing=T[1: Union[Numeric, tuple[Numeric, ...]]],
                          hessian_limen=T[0.9: Numeric])
@FuncTools.attach_attr(docstring=doc.hessian_curvature_detector, info_func=True, entry_tp=dual_ndarray,
                       return_tp=dual_ndarray)
def hessian_curvature_detector(**params):
    _params: TrialDict = TrialDict(**params)
    return _hessian(**_params.trial(**{'~as_detector': params.get('hessian_limen'),  '~as_curvature': False,
                                       '~as_response': False}))


_make_shell = (lambda x: [gs_k := gaussian_kernel(k_shape=x), thre := _get_gs_thre(gs_k, gs_k.ndim),
                          gs_bin := np.zeros(x),
                          [gs_bin.__setitem__(tuple(_), 1) for _ in np.argwhere(gs_k >= thre)],
                          gs_bin - binary_erosion(gs_bin)][-1])


def _segment_test(*, vec_map: ndarray, img_shape: tuple[int, ...], k_shape: tuple[int, ...],
                  segment_threshold: Numeric):
    gs_k: KernelGen = gaussian_kernel(k_shape=k_shape)
    shell = _make_shell(k_shape)
    shell_idx = np.argwhere(shell == 1)
    _into_idx_pairs = [(np.argmin(np.abs(shell_idx-_[0]).sum(axis=1)), np.argmin(np.abs(shell_idx-_[1]).sum(axis=1)))
                       for _ in _make_orthogonal_cursor(shell, gs_k.anchor)]
    pos_idx, neg_idx = np.zeros_like(vec_map), np.zeros_like(vec_map)
    pos_idx[np.where(vec_map > 0)], neg_idx[np.where(vec_map < 0)] = 1, 1
    pos_sum, neg_sum = np.multiply(pos_idx, vec_map).sum(axis=1), np.multiply(neg_idx, vec_map).sum(axis=1)
    msk = np.array([not np.any(np.abs(v) < segment_threshold)
                    for v in np.array([vec_map.T[_, :] for _ in _into_idx_pairs]).T])  # accelerator
    return np.multiply(msk, np.vstack([pos_sum, neg_sum * (-1)]).max(axis=0)).reshape(img_shape)  # auto accelerate


def _fast(*, vec_map: ndarray, img_shape: tuple[int, ...], clipper_thre: tuple[Numeric, Numeric]):
    _tri_msk = _ternarization(vec_map, *clipper_thre)
    pos_idx, neg_idx = np.zeros_like(vec_map), np.zeros_like(vec_map)
    pos_idx[np.where(vec_map > clipper_thre[1])], neg_idx[np.where(vec_map < clipper_thre[0])] = 1, 1
    pos_sum, neg_sum = np.multiply(pos_idx, vec_map).sum(axis=1), np.multiply(neg_idx, vec_map).sum(axis=1)
    return np.vstack([pos_sum, neg_sum * (-1)]).max(axis=0).reshape(img_shape)


_check_fast_thre = (lambda x: all([isinstance(_, Numeric) for _ in x] +
                                  [len(x) == 2]) if hasattr(x, '__iter__') else isinstance(x, float) and 0 < x < 0.5)


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          **{'~in_operator': T['moravec': Literal['moravec', 'harris', 'usan', 'segment', 'fast']],
                             '~get_vector_map': T[False: bool]})
def _spherical_curvature(**params):
    tensor, op = params.get('data').astype(float), params.get('~in_operator')
    k_shape = default_param(params, 'k_shape', tuple(3 for _ in range(tensor.ndim)))
    assert_info_raiser(all([_ >= 3 for _ in k_shape]),
                       ValueError('each dimension of differential operator should be no less than 3'))

    if op == 'moravec':
        order = params.get('norm_order')
        k_shape = tuple(3 for _ in range(tensor.ndim))
        ks = _pairwise_to_center(np.ones(k_shape), tuple(1 for _ in range(tensor.ndim)), True)
        meta = np.array([correlate(tensor, k, output=float, mode=params.get('k_mode'), cval=params.get('k_cval'),
                                   origin=0).ravel() for k in ks]).T
        res = np.linalg.norm(meta, axis=1, ord=order).reshape(tensor.shape)  # scaled

    elif op == 'harris':
        coef, window, sp = params.get('trace_coef'), params.get('clip_window'), params.get('in_spacing')
        sp = sp if hasattr(sp, '__iter__') else tuple(sp for _ in range(len(k_shape)))
        k_base, frac = KernelGen(shape=k_shape, fill=0), [2/(v2-1)*v1 for v1, v2 in zip(sp, k_shape)]
        _k: KernelGen = gaussian_kernel(k_shape=k_shape)
        k_global = _k if window == 'continuous' else _gs_bin(_k, _k.ndim, True)
        ks = [_margin(v1, i) * v2 for i, (v1, v2) in enumerate(zip(_detector_kernels(k_base), frac))]
        ks = [_diff_op(KernelGen(shape=k.shape, replace=k)) for k in ks]
        meta = np.array([correlate(tensor, k, output=float, mode=params.get('k_mode'), cval=params.get('k_cval'),
                                   origin=0).ravel() for k in ks]).T
        m = np.array([correlate(_.reshape(tensor.shape), k_global, output=float, mode=params.get('k_mode'),
                                cval=params.get('k_cval'), origin=0).ravel() for _ in
                      np.array([(v1[..., np.newaxis] @ v1[..., np.newaxis].T).ravel() for v1 in meta]).T]).T
        curvature = np.array([np.linalg.det(_) - coef * (np.trace(_) ** 2) for _ in
                              np.array([_.reshape((k_global.ndim, k_global.ndim)) for _ in m])])
        res = curvature.reshape(tensor.shape)

    elif op == 'usan':
        gs_k, window = gaussian_kernel(k_shape=k_shape), params.get('clip_window')

        if window == 'binomial':
            thre, gs_bin = _get_gs_thre(gs_k, tensor.ndim), np.zeros(k_shape)
            gs_bin[np.where(gs_k >= thre)], gs_bin[tuple(gs_k.anchor)] = 1, 0
            ks = _pairwise_to_center(gs_bin, gs_k.anchor, False)
            ks = [_/(len(ks)) for _ in ks]  # rescaled binary gaussian weights
        else:
            _params: TrialDict = TrialDict(**params)
            gs_k, others = gaussian_kernel(**_params.trial(**{'~other_info': True}))
            power_item = np.log(gs_k) + 0.5 * (np.log(np.linalg.det(others[0])) + others[1] * LOG_2PI)  # to kernel
            _ks = KernelGen(shape=k_shape, replace=np.exp((-1) * (-power_item)**3))
            ks = _pairwise_gs_kernel(_ks)
            frac = _ks.sum() - _ks[tuple(_ks.anchor)]
            ks = [_/frac for _ in ks]  # rescaled general gaussian weights

        meta = np.array([correlate(tensor, k, output=float, mode=params.get('k_mode'), cval=params.get('k_cval'),
                                   origin=0).ravel() for k in ks]).T
        res = (meta.sum(axis=1) * (-1)).reshape(tensor.shape)

    else:  # op in ['segment', 'fast']
        gs_k: KernelGen = gaussian_kernel(k_shape=k_shape)
        ks = _pairwise_to_center(_make_shell(k_shape), gs_k.anchor, False)
        meta = np.array([correlate(tensor, k, output=float, mode=params.get('k_mode'), cval=params.get('k_cval'),
                                   origin=0).ravel() for k in ks]).T

        if params.get('~get_vector_map'):  # branch for further machine learning, FAST detector
            return meta

        if op == 'segment':
            _thre = params.get('segment_threshold')
            _thre = _thre * 100 if isinstance(_thre, float) and 0 < _thre < 1 else _thre
            thre = np.percentile(meta.ravel(), [_thre])[0]
            res = _segment_test(vec_map=meta, img_shape=tensor.shape, k_shape=k_shape, segment_threshold=thre)
        else:  # op is 'fast'
            _thre = params.get('fast_reject_thresholds')
            _thre = [_thre*100, 100 - _thre*100] if not hasattr(_thre, '__iter__') \
                else [_*100 for _ in _thre] if all([0 < _ < 1 for _ in _thre]) else _thre
            thre = np.percentile(meta.ravel(), _thre)
            if clf := params.get('fast_classifier'):  # Callable[[Sequence[0 | Numeric]], Numeric]
                vec_map = np.multiply(meta.__abs__(), _ternarization(meta, *thre))  # __abs__() as ternary
                res = clf(vec_map).reshape(tensor.shape)
            else:
                res = _fast(vec_map=meta, img_shape=tensor.shape, clipper_thre=thre)

    return res


@FuncTools.params_setting(data=T[Null: dual_ndarray], norm_order=T[2: int], k_cval=T[0: Numeric],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']])
@FuncTools.attach_attr(docstring=doc.moravec_response, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def moravec_response(**params):
    _params: TrialDict = TrialDict(**params)
    return _spherical_curvature(**_params.trial(**{'~in_operator': 'moravec'}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], in_spacing=T[1: Union[Numeric, Iterable[Numeric]]],
                          trace_coef=T[0.05: Numeric], clip_window=T['binomial': Literal['binomial', 'continuous']],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0: Numeric])
@FuncTools.attach_attr(docstring=doc.harris_response, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def harris_response(**params):
    _params: TrialDict = TrialDict(**params)
    return _spherical_curvature(**_params.trial(**{'~in_operator': 'harris'}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          clip_window=T['binomial': Literal['binomial', 'continuous']],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']],
                          k_cval=T[0: Numeric])
@FuncTools.attach_attr(docstring=doc.usan_response, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def usan_response(**params):
    _params: TrialDict = TrialDict(**params)
    return _spherical_curvature(**_params.trial(**{'~in_operator': 'usan'}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          segment_threshold=T[0.6: Numeric], k_cval=T[0: Numeric],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']])
@FuncTools.attach_attr(docstring=doc.segment_response, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def segment_response(**params):
    _params: TrialDict = TrialDict(**params)
    return _spherical_curvature(**_params.trial(**{'~in_operator': 'segment', '~get_vector_map': False}))


@FuncTools.params_setting(data=T[Null: dual_ndarray], k_shape=T[None: Optional[tuple[int, ...]]],
                          fast_reject_thresholds=T[(0.4, 0.6): _check_fast_thre],
                          fast_classifier=T[None: Optional[Callable]], k_cval=T[0: Numeric],
                          k_mode=T['reflect': Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap']])
@FuncTools.attach_attr(docstring=doc.fast_response, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def fast_response(**params):
    _params: TrialDict = TrialDict(**params)
    return _spherical_curvature(**_params.trial(**{'~in_operator': 'fast', '~get_vector_map': False}))


__all__ = [func for func in dir() if hasattr(eval(func), 'info_func')] + ['config']


if __name__ == '__main__':
    pass
