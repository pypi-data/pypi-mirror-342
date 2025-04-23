from info.basic.functions import default_param
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null, Numeric
from info.toolbox.libs.operations.logger import exception_logger
from info import docfunc as doc
from pandas import DataFrame
from typing import Generator, Any, Optional, Union
import numpy as np
from scipy.ndimage import label
import os


_warn_msg = 'repeats less than 3, use mean instead, for statistic might not be accurate...'
func = __import__('info.basic.functions', fromlist=['_make_column_name'])
dep = __import__('info.basic.medical', fromlist=['_itk_img'])
_itk_img = getattr(dep, '_itk_img')
_make_column_name = getattr(func, '_make_column_name')
_get_values = getattr(func, '_get_values')
_fea_pick = getattr(func, '_fea_pick')
_is_mask_pair = getattr(dep, '_is_mask_pair')
_superposition = getattr(dep, '_superposition')
_is_enclosed = getattr(dep, '_is_enclosed')
_diff_set = getattr(dep, '_diff_set')
_union_set = getattr(dep, '_union_set')
_points_pair = getattr(dep, '_points_pair')
_apply_spacing = getattr(dep, '_apply_spacing')
_minimum_dis = getattr(dep, '_minimum_dis')
_is_cross = getattr(dep, '_is_cross')
_get_gs_thre = getattr(func, '_get_gs_thre')
gaussian_kernel = __import__('info.toolbox.libs._basic', fromlist=['gaussian_kernel']).gaussian_kernel


def _seg_preprocess(msk: np.ndarray):  # list of bool ndarray
    detector = [sp := tuple(3 for _ in range(msk.ndim)), np.ones(sp)][-1]
    _meta, nums = label(msk, detector)
    return [np.isin(_meta, _ + 1) for _ in range(nums)]


def _local_scope(v: np.ndarray, t: np.ndarray, sp: list[Numeric], r: Numeric = None):
    p1, p2 = np.argwhere(_superposition(v, t)).mean(axis=0), np.argwhere(t).mean(axis=0)
    r = np.linalg.norm(_apply_spacing(p1-p2, sp), ord=2) if r is None else r
    _k_shape = tuple([int((2 * r)/_) for _ in sp])
    gk = gaussian_kernel(k_shape=_k_shape)
    anchor = np.argwhere(gk == np.max(gk))[0]
    axes, thre = [_ for _ in range(gk.ndim)], _get_gs_thre(gk, gk.ndim)
    _meta = np.sign(gk - thre + 1e-10) * 0.5 + 0.5
    # noinspection PyTypeChecker
    meta_msk = np.pad(_meta, tuple((0, ext) for ext in [v1 - v2 for v1, v2 in zip(v.shape, _meta.shape)]))
    _shift = (np.ceil(p1) - anchor).astype(int)
    local_scope = np.roll(meta_msk, shift=_shift, axis=axes).astype(bool)
    return _superposition(v, local_scope)


@FuncTools.params_setting(data=T[Null: Generator], extractor_setting=T[{}: dict[str, Any]],
                          err_file=T[None: Optional[str]], image_types=T[None: Optional[dict[str, dict]]],
                          feature_class=T[None: Optional[dict[str, list[str]]]])
@FuncTools.attach_attr(docstring=doc.radiomics_features, info_func=True, entry_tp=Generator, return_tp=DataFrame)
def radiomics_features(**params):
    radi_prompt = __import__('radiomics', fromlist=['setVerbosity']).setVerbosity
    extractor = __import__('radiomics.featureextractor',
                           fromlist=['RadiomicsFeatureExtractor']).RadiomicsFeatureExtractor
    exe = extractor(**params.get('extractor_setting'))
    conf1, conf2 = params.get('image_types'), params.get('feature_class')
    _ = exe.enableImageTypes(**conf1) if conf1 else exe.enableAllImageTypes()
    exe.enableAllFeatures()  # following customized
    radi_prompt(60)
    has_no_column_names, values, col_names, row_name = True, [], [], []
    err_file = default_param(params, 'err_file', os.path.sep.join([os.getcwd(), 'err_case.log']))
    *_, err_file = err_file.split(os.path.sep)
    err_directory, name = os.path.sep.join(_) if len(_) > 0 else '.', None
    try:
        for name, img, msk, sp in params.get('data'):  # (case_name, img_ndarray, roi_ndarray, spacing)
            try:
                fea = exe.execute(_itk_img(img, sp, None, None), _itk_img(msk, sp, None, None))
                if has_no_column_names:
                    col_names = _make_column_name(fea)
                    has_no_column_names = False
                values.append(_get_values(fea))
                row_name.append(name)
            except (Exception, ) as err:
                exception_logger(data=(name, err), directory=err_directory, to_file=err_file)
    except (Exception, ) as err:
        exception_logger(data=(f'last case {name} before interrupt', err), directory=err_directory, to_file=err_file)

    res = DataFrame([])

    if len(col_names) > 0:
        if conf2:
            idx = np.array([_fea_pick(_, conf2) for _ in col_names])
            res = DataFrame(np.array(values)[:, idx], index=row_name, columns=np.array(col_names)[idx])
        else:
            res = DataFrame(np.array(values), index=row_name, columns=col_names)

    # modify the incorrect result (maybe bug?) from pyradiomics
    # TODO: 1. report to git; 2. version BUG: issue 828 https://github.com/AIM-Harvard/pyradiomics/issues/828

    return res


@FuncTools.params_setting(data=T[Null: _is_mask_pair], in_spacing=T[None: Optional[Union[list[Numeric], np.ndarray]]],
                          scope_radius=T[None: Optional[Numeric]],
                          **{'~differential_tolerance': T[2: lambda x: isinstance(x, int) and x > 0]})
@FuncTools.attach_attr(docstring=doc.vascular_invasion, info_func=True, entry_tp=tuple[np.ndarray, np.ndarray],
                       return_tp=dict[bool, Union[Numeric, list[Numeric]]])
def vascular_invasion(**params):
    v, t = params.get('data')
    s = _superposition(v, t)
    sp = default_param(params, 'in_spacing', [1 for _ in range(v.ndim)])
    _tol, _scope = params.get('~differential_tolerance'), params.get('scope_radius')

    if True not in s:
        res = {False: _minimum_dis(v, t, sp)}

    elif s.sum() in [v.sum(), v.sum()-1]:  # fully enclosed, internally tangent, cut-through
        # TODO: activate improved cut-through determination (deprecate _is_cross temporarily)
        res = {True: 2 * np.pi}

    elif s.sum() == 1:  # externally tangent
        res = {True: 0}

    else:  # partially closed
        segs = _seg_preprocess(s)

        if len(segs) == 1:  # single superposition region

            _c = _local_scope(v, t, sp, _scope)  # TODO: Efficiency optimization in this step for supporting 3D
            centroid = np.argwhere(_c).mean(axis=0)

            # _points_pair should apply voxel spacing
            _v1, _v2 = _points_pair(_diff_set(v, t), sp) if (_inv := _is_enclosed(_c, t)) else _points_pair(segs[0], sp)
            v1, v2 = _apply_spacing(_v1 - centroid, sp), _apply_spacing(_v2 - centroid, sp)
            theta = np.arccos(np.dot(v1, v2) / np.prod(np.linalg.norm(np.array([v1, v2]), ord=2, axis=1)))
            theta = 2 * np.pi - theta if _inv else theta

            res = {True: theta}

        else:  # multiple superposition regions
            _base = _diff_set(v, t)
            _res = [vascular_invasion(data=(_union_set(_, _base), t), in_spacing=sp) for _ in segs]
            res = {True: [_.get(True) for _ in _res]}

    return res


__all__ = ['radiomics_features', 'vascular_invasion']


if __name__ == '__main__':
    pass
