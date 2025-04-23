from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null, Numeric
from info.basic.functions import default_param, assert_info_raiser
from info.toolbox.libs._basic import gaussian_kernel
import info.docfunc as doc
from typing import Union, Optional, Generator, Iterable, Literal
from warnings import warn
from tensorly.decomposition import parafac
from tensorly import validate_cp_rank, cp_to_tensor
from scipy.interpolate import interp1d
from numpy import ndarray as np_ndarray
import numpy
try:
    cp_ndarray = __import__('cupy', fromlist=['ndarray']).ndarray
except ImportError as _:
    cp_ndarray = np_ndarray
bsc = __import__('info.toolbox.libs._basic', fromlist=['ndarray'])
ndarray = getattr(bsc, 'ndarray')
np = getattr(bsc, 'np')
_basic_config = getattr(bsc, 'config')
fun = __import__('info.basic.functions', fromlist=['_is_inside'])
_is_inside = getattr(fun, '_is_inside')
_get_gs_thre = getattr(fun, '_get_gs_thre')
_calculate_transfer = getattr(fun, '_calculate_transfer')
ndimage = __import__('scipy.ndimage', fromlist=['label'])
label = getattr(ndimage, 'label')
binary_erosion = getattr(ndimage, 'binary_erosion')
binary_dilation = getattr(ndimage, 'binary_dilation')
dual_ndarray = Union[np_ndarray, cp_ndarray]


class _Config:

    verbosity = False

    def __init__(self):
        global np, ndarray, label, binary_erosion, binary_dilation
        import numpy as np
        from numpy import ndarray
        from scipy.ndimage import label, binary_erosion, binary_dilation
        _basic_config.reset(device='cpu')
        self.device_ = 'cpu'
        print(np, ndarray, label, binary_erosion, binary_dilation, _basic_config.device_) if self.verbosity else ...

    @FuncTools.params_setting(device=T['cpu': Literal['cpu', 'gpu']])
    def reset(self, **params):
        self.device_ = params.get('device')
        global np, ndarray, label, binary_erosion, binary_dilation
        if self.device_ == 'cpu':
            import numpy as np
            from numpy import ndarray
            from scipy.ndimage import label, binary_erosion, binary_dilation
            _basic_config.reset(device='cpu')
            print(np, ndarray, label, binary_erosion, binary_dilation, _basic_config.device_) if self.verbosity else ...
        if self.device_ == 'gpu':
            try:
                np = __import__('cupy')
                ndarray = __import__('cupy', fromlist=['ndarray']).ndarray
                label = __import__('cupyx.scipy.ndimage', fromlist=['label']).label
                binary_erosion = __import__('cupyx.scipy.ndimage', fromlist=['binary_erosion']).binary_erosion
                binary_dilation = __import__('cupyx.scipy.ndimage', fromlist=['binary_dilation']).binary_dilation
                _basic_config.reset(device='gpu')
            except ImportError as _:
                warn('Cuda or Cupy is not available, reset default device as cpu...')
                self.reset(device='cpu')
            print(np, ndarray, label, binary_erosion, binary_dilation, _basic_config.device_) if self.verbosity else ...


config = _Config()


@FuncTools.params_setting(data=T[Null: lambda x: x.dtype == bool], prob_nums=T[Null: int], prob_radius=T[Null: int],
                          in_spacing=T[None: Optional[Iterable[Numeric]]])
@FuncTools.attach_attr(docstring=doc.prober, info_func=True, entry_tp=dual_ndarray, return_tp=Generator)
def prober(**params):
    msk, nums, r, sp = params.get('data'), params.get('prob_nums'), params.get('prob_radius'), params.get('in_spacing')
    dims, shape = msk.ndim, msk.shape
    radius = [round(r/_sp) for _sp in sp] if sp is not None else [r for _ in range(dims)]
    g_k = gaussian_kernel(k_shape=tuple(1+2*_r for _r in radius))  # only 1 maximum guaranteed
    anchor, _centers = np.argwhere(g_k == np.max(g_k))[0], np.argwhere(msk == 1)
    centers, axes, thre = _centers - anchor, [_ for _ in range(dims)], _get_gs_thre(g_k, dims)
    _meta_msk, _len_c = np.sign(g_k-thre + 1e-10)*0.5 + 0.5, len(centers)  # for tangent = 1
    meta_msk = np.pad(_meta_msk, tuple((0, expand) for expand in [v1-v2 for v1, v2 in zip(shape, _meta_msk.shape)]))
    while nums:  # Monte Carlo sampling
        _shift = centers[tuple(np.random.choice(_len_c, 1))]
        _mask = np.roll(meta_msk, shift=_shift, axis=axes)
        if _is_inside(msk, _mask):
            nums -= 1
            yield _mask.astype(bool)


@FuncTools.params_setting(data=T[Null: dual_ndarray], grid_nums=T[7: Union[int, list[int]]])
@FuncTools.attach_attr(docstring=doc.grid_mesh, info_func=True, entry_tp=dual_ndarray, return_tp=Generator)
def grid_mesh(**params):
    x, _grid_nums = params.get('data'), params.get('grid_nums')
    _idx, grid_nums = np.argwhere(x), [_grid_nums for _ in range(x.ndim)] if isinstance(_grid_nums, int) else _grid_nums
    _start, _end = _idx.min(axis=0), _idx.max(axis=0) + 1
    _pad = [v2 - (v1 % v2) for v1, v2 in zip(_end - _start, grid_nums)]
    _pads = [(_m := int((_ - 1) / 2), _m + 1) if _ % 2 else (_m := _ / 2, _m) for _ in _pad]
    _start, _end = (np.array([v1 - v2[0] for v1, v2 in zip(_start, _pads)]).astype(int),
                    np.array([v1 + v2[1] for v1, v2 in zip(_end, _pads)]).astype(int))
    cor = [[v1 + _ * ((v2 - v1) // v3) for _ in range(v3 + 1)] for v1, v2, v3 in zip(_start, _end, grid_nums)]
    uni_vec = np.array([np.diff(_)[0] for _ in cor])
    grid_points = np.array([_.ravel() for _ in np.meshgrid(*cor)]).T
    for __start in grid_points:
        if np.all([v1 <= v2 for v1, v2 in zip(__start + uni_vec, _end)]):
            slices = [slice(v1, v2) for v1, v2 in zip(__start, __start + uni_vec)]
            if np.any(x[tuple(slices)]):  # labeled area involved
                _seg = np.zeros_like(x)
                _seg[tuple(slices)] = 1
                yield x * _seg.astype(bool)


@FuncTools.params_setting(data=T[Null: dual_ndarray], detector=T[None: Optional[dual_ndarray]])
@FuncTools.attach_attr(docstring=doc.connected_domain, info_func=True, entry_tp=dual_ndarray, return_tp=Generator)
def connected_domain(**params):
    msk = params.get('data')
    detector = default_param(params, 'detector', [sp := tuple(3 for _ in range(msk.ndim)),
                                                  g_k := gaussian_kernel(k_shape=sp),
                                                  thre := _get_gs_thre(g_k, msk.ndim),
                                                  np.sign(g_k-thre + 1e-10)*0.5 + 0.5][-1])
    _meta, nums = label(msk, detector) if msk.dtype == bool else (msk, len(np.unique(msk))-1)
    return (np.isin(_meta, _+1) for _ in range(nums))


@FuncTools.params_setting(data=T[Null: dual_ndarray], new_size=T[Null: tuple[int, ...]],
                          interp_method=T['nearest': Literal['linear', 'nearest', 'nearest-up', 'zero', 'slinear',
                          'quadratic', 'cubic', 'previous', 'next']])
@FuncTools.attach_attr(docstring=doc.seg_resize, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def seg_resize(**params):
    data, new_size, method = (params.get('data').copy(), params.get('new_size'),
                              params.get('interp_method'))
    if hasattr(data, 'get'):  # calculation through cpu
        data = data.get()
    data = data + numpy.random.random(data.shape) * 1e-5  # to float, escape LinAlgError of Singular matrix

    core, mats = parafac(data, validate_cp_rank(data.shape))
    org_x = [numpy.array([_ for _ in range(dim)]) for dim in data.shape]
    new_x = [numpy.linspace(0, org_x[_][-1], new_size[_]) for _ in range(len(new_size))]
    n_mats = tuple(numpy.array([interp1d(org_x[nd], _, kind=method)(new_x[nd]) for _ in mats[nd].T]).T
                   for nd in range(len(mats)))
    ref, res = np.array(cp_to_tensor((core, n_mats))), np.zeros(new_size)
    res[np.where(ref > 0.5)] = 1
    return res.astype(bool)


@FuncTools.params_setting(data=T[Null: lambda x: x.dtype == bool], norm=T[1: Union[Numeric, Iterable[Numeric]]],
                          in_spacing=T[None: Optional[Iterable[Numeric]]])
@FuncTools.attach_attr(docstring=doc.erosion, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def erosion(**params):
    res, norm = params.get('data').copy(), params.get('norm')
    sp = default_param(params, 'in_spacing', tuple(1 for _ in range(res.ndim)))
    assert_info_raiser(res.ndim == len(norm) if hasattr(norm, '__iter__') else True,
                       ValueError('assignment for norm not match dimensions of data'))
    return binary_erosion(res, _calculate_transfer(res, norm, gaussian_kernel, sp), 1).astype(bool)


@FuncTools.params_setting(data=T[Null: lambda x: x.dtype == bool], norm=T[1: Union[Numeric, Iterable[Numeric]]],
                          in_spacing=T[None: Optional[Iterable[Numeric]]])
@FuncTools.attach_attr(docstring=doc.dilation, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def dilation(**params):
    res, norm = params.get('data').copy(), params.get('norm')
    sp = default_param(params, 'in_spacing', tuple(1 for _ in range(res.ndim)))
    assert_info_raiser(res.ndim == len(norm) if hasattr(norm, '__iter__') else True,
                       ValueError('assignment for norm not match dimensions of data'))
    return binary_dilation(res, _calculate_transfer(res, norm, gaussian_kernel, sp), 1).astype(bool)


@FuncTools.params_setting(data=T[Null: lambda x: x.dtype == bool],
                          instances=T[Null: Union[dual_ndarray, list[dual_ndarray]]])
@FuncTools.attach_attr(docstring=doc.intersection, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def intersection(**params):
    org, res = params.get('data'), params.get('instances')
    res = [res] if not isinstance(res, list) else res
    res = [_.astype(int) for _ in res]
    res.append(org)
    return np.isin(np.sum(np.array(res), axis=0), len(res))


@FuncTools.params_setting(data=T[Null: lambda x: x.dtype == bool],
                          instances=T[Null: Union[dual_ndarray, list[dual_ndarray]]])
@FuncTools.attach_attr(docstring=doc.union, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def union(**params):
    org, res = params.get('data'), params.get('instances')
    res = [res] if not isinstance(res, list) else res
    res = [_.astype(int) for _ in res]
    res.append(org)
    return np.isin(np.sum(np.array(res), axis=0), 0, invert=True)


@FuncTools.params_setting(data=T[Null: lambda x: x.dtype == bool],
                          instances=T[Null: Union[dual_ndarray, list[dual_ndarray]]])
@FuncTools.attach_attr(docstring=doc.difference, info_func=True, entry_tp=dual_ndarray, return_tp=dual_ndarray)
def difference(**params):
    org, res = params.get('data'), params.get('instances')
    res = [res] if not isinstance(res, list) else res
    res = union(data=np.zeros_like(org), instances=[_.astype(int) for _ in res]).astype(int)
    return np.isin(org.astype(int)-res, 1)


def _reserve_former(x):
    res = np.zeros_like(x)
    idx = np.arange(len(x)), x.argmax(axis=1)
    res[idx] = x[idx]
    return res


def _msk_geodesic_distance(x):
    res = x.astype(int) if not x.dtype == int else x
    ref = x.copy()
    while np.sum(ref := binary_erosion(ref)) != 0:
        res += ref.astype(int)
    return -res


_local_max = (lambda x: np.amax(x[np.where(x != 0)]))


class _Watershed:

    def __init__(self, mask, seeds, geodesic=None, _reserve_dup: Literal['former', 'later'] = 'former'):
        self.mask, self.seed = mask, seeds.astype(int)
        self.nums, self.shape = np.unique(self.seed)[1:], self.seed.shape
        self.geo = _msk_geodesic_distance(mask) if geodesic is None else geodesic * mask
        self._save_dup, self._tmp = _reserve_dup, None

    def _get_hollows(self):
        res = np.array([_local_max(np.isin(self.seed, _) * self.geo) for _ in self.nums])
        return np.where(res == np.amin(res))[0] + 1

    def _update_labels(self):
        idx = self._get_hollows()
        self._tmp = np.array([(binary_dilation(np.isin(self.seed, _)) ^ np.isin(self.seed, _)) if _ in idx
                              else np.isin(self.seed, _) for _ in self.nums])  # shell or label
        self._tmp = self._remove_conflict(self._tmp)
        self._tmp = np.array([self._fill_step(self._tmp[_-1], _) if _ in idx else np.isin(self.seed, _) * _ for _
                              in self.nums])
        self.seed = np.sum(self._tmp, axis=0)

    def _remove_conflict(self, m):
        temp = np.array([_.ravel() for _ in m]).T
        temp = _reserve_former(temp) if self._save_dup == 'former' else np.flip(_reserve_former(np.flip(temp, axis=1)),
                                                                                axis=1)
        return np.array([_.reshape(self.shape) * self.mask for _ in temp.T])

    def _fill_step(self, m, idx):
        cell = np.isin(self.seed, idx).astype(int)

        if len(np.unique(m)) > 1:  # else no possible position for shell
            _ind = np.argwhere(m)
            other_cells = np.argwhere(np.isin(self.seed, [_ for _ in self.nums if _ != idx]))
            _ind = np.array([_ for _ in _ind if np.linalg.norm(other_cells - _, ord=2, axis=1).min() != 0])

            if len(_ind) > 0:  # else no update necessary
                vals = self.geo[tuple(_ind.T)]
                _pos = _ind[np.where(vals == np.min(vals))]
                cell[tuple(_pos.T)] = 1  # update position(s)

        return cell * idx

    def flooding(self):
        _tmp = self.seed.astype(bool).sum()
        while [self._update_labels(), (_tmp1 := self.seed.astype(bool).sum()) != _tmp][-1]:  # not converge
            _tmp = _tmp1


@FuncTools.params_setting(data=T[Null: lambda x: x.dtype == bool], flood_seeds=T[Null: dual_ndarray],
                          flood_geography=T[None: Optional[dual_ndarray]], label_output=T[True: bool],
                          **{'~reserve_duplicate': T['former': Literal['former', 'later']]})
@FuncTools.attach_attr(docstring=doc.watershed, info_func=True, entry_tp=dual_ndarray,
                       return_tp=Union[dual_ndarray, Generator[dual_ndarray, None, None]])
def watershed(**params):
    seg, seed, geo, _reserve = (params.get('data'), params.get('flood_seeds'), params.get('flood_geography'),
                                params.get('~reserve_duplicate'))
    wt = _Watershed(seg, seed, geo, _reserve)
    wt.flooding()
    return wt.seed if params.get('label_output') else connected_domain(data=wt.seed)


__all__ = ['config', 'prober', 'grid_mesh', 'connected_domain', 'seg_resize', 'erosion', 'dilation', 'intersection',
           'union', 'difference', 'watershed']


if __name__ == '__main__':
    pass
