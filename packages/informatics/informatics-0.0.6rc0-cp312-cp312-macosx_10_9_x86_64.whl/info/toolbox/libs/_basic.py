# static import:
from info.basic.core import TrialDict
from info.basic.functions import assert_info_raiser, default_param
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null, Numeric
import info.docfunc as doc
from typing import Tuple, List, Sequence, Optional, Union, Literal
from scipy.stats import multivariate_normal  # scipy scopy only
from warnings import warn
import numpy
# init for dynamic import:
import numpy as _np
from numpy import ndarray as _ndarray
np, ndarray = _np, _ndarray


class _Config:

    verbosity = False

    def __init__(self):
        global np, ndarray
        import numpy as np
        from numpy import ndarray
        self.device_ = 'cpu'
        print(np, ndarray) if self.verbosity else ...

    @FuncTools.params_setting(device=T['cpu': Literal['cpu', 'gpu']])
    def reset(self, **params):
        self.device_ = params.get('device')
        global np, ndarray
        if self.device_ == 'cpu':
            import numpy as np
            from numpy import ndarray
            print(np, ndarray) if self.verbosity else ...
        if self.device_ == 'gpu':
            try:
                np = __import__('cupy')
                ndarray = __import__('cupy', fromlist=['ndarray']).ndarray
            except ImportError as _:
                if self.verbosity:
                    warn('Cuda or Cupy is not available, reset default device as cpu...')
                self.reset(device='cpu')
            print(np, ndarray) if self.verbosity else ...


config = _Config()
PI2 = 2 * np.pi
LOG_2PI = np.log(PI2)


class _KernelGen(ndarray):

    def __new__(cls, shape: Tuple,
                dtype: Optional[type] = int,
                buffer: Optional[ndarray] = None,
                offset: Optional[int] = 0,
                strides: Optional[Tuple] = None,
                order: Optional[Literal['C', 'F']] = None,
                origin: Union[int, Sequence[int]] = 0,
                fill: Optional[Numeric] = 1,
                replace: Optional[ndarray] = None,
                *_1,  **_2):

        if config.device_ == 'gpu':
            obj: ndarray = np.ndarray(shape)
        else:
            obj: ndarray = super().__new__(cls, shape, dtype, buffer, offset, strides, order)

        if fill:
            obj: ndarray = np.full_like(obj, fill, dtype=type(fill))
        if replace is not None:
            assert_info_raiser(obj.shape == replace.shape,
                               TypeError(f'{obj} & {replace} should be of the identical shape'))
            obj: ndarray = np.zeros_like(obj) + replace
        _ref1 = np.array([_ for _ in range(numpy.prod(obj.shape))])
        _ref2 = _ref1.reshape(obj.shape)
        _ = np.array([_ * .5 for _ in obj.shape])

        obj.rela_anchor = [np.array(origin) if hasattr(origin, '__len__') else np.ones_like(_) * origin][0]
        obj.center = _ - 0.5  # centered position, float element
        obj.anchor = (np.ceil(obj.center) + obj.rela_anchor).astype(dtype=int)  # anchor position, int element
        obj.anchor_id = np.where(_ref1 == _ref2[tuple(obj.anchor)])[0][0]  # anchor position in ravel, int
        obj.rela_pos_rv = np.array([np.argwhere(_ref2 == item)[0] for item in _ref1]) - obj.center  # raveled indices
        return obj


@FuncTools.attach_attr(docstring=doc.KernelGen)
class KernelGen(_KernelGen):
    pass


@FuncTools.params_setting(k_shape=T[Null: tuple[int, ...]])
@FuncTools.attach_attr(docstring=doc.averaging_kernel)
def averaging_kernel(**params) -> KernelGen:
    _res = np.ones(shape=params.get('k_shape'))
    _sub = _res / _res.sum()
    return KernelGen(shape=_sub.shape, replace=_sub)


@FuncTools.params_setting(k_shape=T[Null: tuple[int, ...]], k_mu=T[None: Optional[ndarray]],
                          k_sigma=T[None: Optional[ndarray]])
@FuncTools.attach_attr(docstring=doc.gaussian_kernel)
def gaussian_kernel(**params) -> Union[KernelGen, Tuple[KernelGen, List[Union[ndarray, int]]]]:
    res: KernelGen = KernelGen(shape=params.get('k_shape'))
    _idx = res.rela_pos_rv
    mu, sigma = (default_param(params, 'k_mu', np.zeros_like(res.center)),
                 default_param(params, 'k_sigma', np.diag(np.array(res.shape))))
    if config.device_ == 'gpu':
        mu, sigma, _idx = mu.get(), sigma.get(), _idx.get() if hasattr(_idx, 'get') else _idx
    mvn = multivariate_normal(mean=mu, cov=sigma, allow_singular=True)  # singular sigma
    _res = np.array([mvn.pdf(item) for item in _idx]).reshape(res.shape)
    if params.get('~other_info', False):
        other_info = [np.array(sigma), mvn.cov_object.rank]  # cov_info to cov_object in scipy ver1.10.1
        return KernelGen(shape=_res.shape, replace=_res), other_info
    else:
        _sub = _res / _res.sum()
        return KernelGen(shape=_sub.shape, replace=_sub)


@FuncTools.params_setting(k_shape=T[Null: tuple[int, ...]])
@FuncTools.attach_attr(docstring=doc.laplacian_of_gaussian_kernel)
def laplacian_of_gaussian_kernel(**params) -> KernelGen:
    _params: TrialDict = TrialDict(**params)
    gs_k, others = gaussian_kernel(**_params.trial(**{'~other_info': True}))
    power_item = np.log(gs_k) + 0.5 * (np.log(np.linalg.det(others[0])) + others[1] * LOG_2PI)  # to kernel
    item1, item2 = 1 + power_item, np.exp(power_item)
    _sub = -np.multiply(item1, item2)
    return KernelGen(shape=_sub.shape, replace=_sub)


def _spatial_sine(*, k_shape, orientation, wave_length: Numeric = PI2, phase: Numeric = 0):
    _meta, _unit = np.ones(k_shape), orientation / np.linalg.norm(orientation, ord=2)
    axes = np.argwhere(_meta)
    modal = np.array([np.dot(_, _unit) for _ in axes])
    p = np.arctan2(modal, np.linalg.norm(axes, axis=1, ord=2))
    return np.array([np.sin((PI2*v1)/wave_length + v2 + phase) for v1, v2 in zip(modal, p)]).reshape(k_shape)


def _spatial_cosine(*, k_shape, orientation, wave_length: Numeric = PI2, phase: Numeric = 0):
    return _spatial_sine(k_shape=k_shape, orientation=orientation, wave_length=wave_length, phase=np.pi*0.5-phase)


@FuncTools.params_setting(k_shape=T[Null: tuple[int, ...]], k_rescale=T[1: Numeric],
                          k_orientation=T[Null: list[Numeric]], k_wavelength=T[PI2: Numeric], k_phase=T[0: Numeric])
@FuncTools.attach_attr(docstring=doc.gabor_kernel)
def gabor_kernel(**params) -> KernelGen:
    _shape, scale, wav_len, phase, direction = (params.get('k_shape'), params.get('k_rescale'),
                                                params.get('k_wavelength'), params.get('k_phase'),
                                                params.get('k_orientation'))
    gk = gaussian_kernel(k_shape=_shape, k_sigma=np.diag(np.array(_shape)) * scale)
    k_real = gk * _spatial_cosine(k_shape=_shape, orientation=direction, wave_length=wav_len, phase=phase)
    k_image = gk * _spatial_sine(k_shape=_shape, orientation=direction, wave_length=wav_len, phase=phase)
    return KernelGen(shape=_shape, replace=k_real + k_image * 1j)


__all__ = ['config', 'KernelGen', 'averaging_kernel', 'gaussian_kernel', 'laplacian_of_gaussian_kernel', 'gabor_kernel']


if __name__ == '__main__':
    pass
