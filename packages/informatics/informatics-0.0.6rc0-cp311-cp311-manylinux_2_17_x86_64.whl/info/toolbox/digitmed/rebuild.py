from info.basic.functions import assert_info_raiser, default_param
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null, Numeric
from info.basic.core import SingleMap
from info.toolbox.libs import io
from info.toolbox.libs.tensor.numeric import resize
import info.docfunc as doc
from scipy.ndimage import binary_fill_holes
from typing import Iterable, Optional, List, Union, Tuple, Callable, Literal, Generator, Any
from itertools import permutations
from info.basic.medical import Itk
from functools import cached_property, partial
from dataclasses import dataclass
import copy
import warnings
from numpy import ndarray
import numpy as np
import os
import re


fun = __import__('info.basic.functions', fromlist=['_float_timestamp'])
_pydicom = __import__('pydicom', fromlist=['dcmread'])
dcmread = getattr(_pydicom, 'dcmread')
InvalidDicomError = getattr(getattr(_pydicom, 'errors'), 'InvalidDicomError')
Image = Itk.SimpleITK.Image
_float_timestamp = getattr(fun, '_float_timestamp')
_save = getattr(fun, '_save')
_pos = getattr(fun, '_pos')
_connect = getattr(fun, '_connect')
_vertex_to_edge = getattr(fun, '_vertex_to_edge')
_warn = getattr(fun, '_warn')


struct_config = {
    'roi_name_k': ['StructureSetROISequence', 'ROIName'],
    'roi_number_k': ['StructureSetROISequence', 'ROINumber'],
    'contour_sequence_k': ['ROIContourSequence', 'ContourSequence'],
    'referenced_roi_number_k': ['ROIContourSequence', 'ReferencedROINumber'],
}

SimpleITK_config = {
    'loader': 'SimpleITK',
    'series_k': "0020|000e",
    'instance_k': "0008|0018",
    'image_orientation_k': "0020|0037",
    'pixel_spacing_k': "0028|0030",
    'image_position_k': "0020|0032",
    'spacing_between_slices_k': "0018|0088",
    'axis_order': 'zyx',
}

pydicom_config = {
    'loader': 'pydicom',
    'series_k': 'SeriesInstanceUID',
    'instance_k': 'SOPInstanceUID',
    'image_orientation_k': 'ImageOrientationPatient',
    'pixel_spacing_k': 'PixelSpacing',
    'image_position_k': 'ImagePositionPatient',
    'spacing_between_slices_k': 'SpacingBetweenSlices',
    'axis_order': 'zyx',
}

ROIName = struct_config.get('roi_name_k')
ROINumber = struct_config.get('roi_number_k')
ContourSequence = struct_config.get('contour_sequence_k')
ReferencedROINumber = struct_config.get('referenced_roi_number_k')


def _roi_seq_to_ndarray(*, data, __data_key, __coord: Tuple[ndarray, ndarray, ndarray],
                        __order: Tuple[int] = (2, 1, 0), __z_pos: int = 0):
    """default order (1, 0, 2) to 'xyz', makes '__oder' matches DcmSeries._intrinsic_order()"""
    seq_list = [np.array(_, dtype=float).reshape((-1, 3)).T[np.array((1, 0, 2))][np.array(__order)]
                for _ in [dcm_attr_loader(data=_, attr_path=__data_key) for _ in data]]
    res = np.zeros(tuple(len(_) for _ in __coord))

    def _swap_xy(obj: list, fix_axis: int):
        _ = obj.pop(fix_axis)
        obj1 = obj[::-1]
        obj1.insert(fix_axis, _)
        return obj1

    __coord = _swap_xy(list(__coord), __z_pos)  # swap x and y for _pos call
    vertex_pos = [np.array([[_pos(v, __coord[idx]) for idx, v in enumerate(_)] for _ in _v.T]) for _v in seq_list]
    edge_pos = [_vertex_to_edge(_) for _ in vertex_pos]

    for pos_set in edge_pos:
        for pos in pos_set:
            res[tuple(pos)] = 1

    _res = [_.sum(axis=__z_pos) for _ in np.split(res, res.shape[__z_pos], axis=__z_pos)]
    return np.stack([binary_fill_holes(_) if _.sum() != 0 else _ for _ in _res], axis=__z_pos)


def _map_roi_from_names(*, data: List[str], struct_file: str, roi_constructor: Callable = lambda x: x,
                        name_number_path: Tuple[List[str]] = (ROIName, ROINumber),
                        contour_number_path: Tuple[List[str]] = (ContourSequence, ReferencedROINumber)):
    name, s1 = np.array(dcm_attr_loader(data=struct_file, attr_path=copy.deepcopy(name_number_path)), dtype=object)
    seqs, s2 = dcm_attr_loader(data=struct_file, attr_path=copy.deepcopy(contour_number_path))
    p_num, s2 = [s1[_][0] if s1[_].size > 0 else None for _ in [np.where(name == v)[0] for v in data]], np.array(s2)
    return [roi_constructor(data=seqs[_]) if _ is not None else None for _ in
            [np.where(s2 == _)[0][0] if _ else None for _id, _ in enumerate(p_num)]]


def _dose_volume_hist(dose_map: ndarray, msk: ndarray, seps: int) -> tuple[ndarray, ndarray]:
    res, axis = dose_map[msk == 1], np.linspace(0, 100, seps)
    _points = np.percentile(res, axis)
    nums = int(np.floor(np.min(_points)))
    _y, _x = np.array([100 for _ in range(nums + 1)]), np.linspace(0, nums, nums + 1)
    return np.concatenate([_x, _points]), np.concatenate([_y, axis[::-1]])


def _dvh_name_map(*, data: Union[list[str], dict[str, ndarray]], __dose: ndarray, __msk_trans: Callable,
                  __seps: int = 100) -> list[tuple[ndarray, ndarray]]:
    if isinstance(data, list):
        res = [_dose_volume_hist(__dose, __msk_trans(data=[_])[0], __seps) for _ in data]
    else:
        res = [_dose_volume_hist(__dose, __msk_trans(data=[v])[0], __seps) for k, v in data.items()]
    return res


@dataclass
class _Dose:
    affine: ndarray
    rcs_array: ndarray
    axis_order: tuple[int, int, int]

    @property
    def rcs_spacing(self):
        return np.linalg.norm(self.affine.T[:3], axis=1, ord=2)[np.array(self.axis_order)]

    @property
    def rcs_origin(self):
        return self.affine.T[-1][:3][np.array(self.axis_order)]

    @property
    def rcs_coordinate(self):
        shape = self.rcs_array.shape
        return tuple(np.array([inner for inner in range(shape[_])]) * self.rcs_spacing[_] + self.rcs_origin[_]
                     for _ in range(len(shape)))


class _DcmLoader:

    def __init__(self, loader: str):
        assert_info_raiser(loader in ['pydicom', 'SimpleITK'],
                           ValueError("data loader should be assigned as 'pydicom' or 'SimpleITK'"))
        self.loader = loader

    @property
    def robust_header_loader(self):
        if self.loader == 'pydicom':
            def func(x):
                try:
                    res = dcmread(x, force=True)
                except InvalidDicomError as _:
                    res = 'err_tag'
                return res
            return func
        if self.loader == 'SimpleITK':
            def func(x):
                try:
                    res = Itk.ReadImage(x)
                except RuntimeError as _:
                    res = 'err_tag'
                return res
            return func

    @property
    def ndarray_image_loader(self):
        if self.loader == 'pydicom':
            def func(x):
                return x.pixel_array.astype('int16') - 1024  # match value of SimpleITK
            return func
        if self.loader == 'SimpleITK':
            def func(x):
                res = Itk.GetArrayFromImage(x)
                return res[0] if len(res) == 1 else res  # support for dose
            return func

    @property
    def attribute_loader(self):
        if self.loader == 'pydicom':
            def func(x, attr: Union[str, List[str]]):
                attr, res = [attr] if isinstance(attr, str) else attr, []

                def _recursive_attr_prob(prob, _attr: List[str]):
                    k = '_empty_prob'
                    if len(_attr) > 0:
                        k = _attr.pop(0)
                    else:
                        res.append(prob)
                    prob = [_ for _ in prob] if hasattr(prob, '_list') else [prob]
                    prob = [eval(f'_.{k}') for _ in prob if hasattr(_, k)]
                    for _item in prob:
                        _recursive_attr_prob(_item, attr)
                _recursive_attr_prob(x, attr)
                return res[0] if len(res) == 1 else res
            return func
        if self.loader == 'SimpleITK':
            def func(x, attr):
                res = x.GetMetaData(attr)
                if attr in {"0028|1050", "0028|1051"}:
                    res = [int(_) for _ in res.split(os.path.sep)]
                elif attr in {"0020|0037", "0018|9313", "0018|9318", "0018|9352", "0020|0032", "0028|0030",
                              "3004|000c"}:
                    res = [float(_) for _ in res.split(os.path.sep)]
                elif attr in {"0008|0008", "0018|1210", "0028|1055"}:
                    res = [_ for _ in res.split(os.path.sep)]
                elif attr in {"0018|0050", "0018|0088", "0018|9345", "0020|1041", "0028|1053", "0018|0090",
                              "0018|1100", "3004|000e"}:
                    res = float(res) if len(res) > 0 else ''
                elif attr in {"0018|0060", "0018|1151", "0018|1152", "0020|0011", "0028|0002", "0028|0010",
                              "0028|0011", "0028|0100", "0028|0101", "0028|0102", "0028|0103", "0028|1052"}:
                    res = int(res) if len(res) > 0 else ''
                return res
            return func

    @property
    def all_keys(self):
        if self.loader == 'pydicom':
            def func(x):
                return x.dir()
            return func
        if self.loader == 'SimpleITK':  # default IO use GDCMImageIO; weak performance in construction for dicom header
            def func(x):
                return x.GetMetaDataKeys()
            return func


def _intrinsic_order(x: dict):
    a, b, c = x.get('axis_order')
    order = (0, 1, 2)
    for v1, v2 in zip(permutations('xyz'), permutations((0, 1, 2))):
        if (a, b, c) == v1:
            order = v2
    return order


def _rcs_spacing(x: ndarray, order: tuple[int, int, int]):
    return np.linalg.norm(x.T[:3], axis=1, ord=2)[np.array(order)]


def _rcs_origin(x: ndarray, order: tuple[int, int, int]):
    return x.T[-1][:3][np.array(order)]


def _rcs_array(x: Image, order: tuple[int, int, int]):
    _meta = Itk.GetArrayFromImage(x).transpose((1, 2, 0))  # init & not change rcs
    return _meta.transpose(order)


def _rcs_coordinate(x: ndarray, spacing: ndarray, origin: ndarray):
    shape = x.shape
    return tuple(np.array([inner for inner in range(shape[_])]) * spacing[_] + origin[_] for _ in range(len(shape)))


_pydicom_engin = _DcmLoader(loader='pydicom')
_f_head, _f_attr = _pydicom_engin.robust_header_loader, _pydicom_engin.attribute_loader


@FuncTools.params_setting(data=T[Null: lambda x: os.path.exists(x) if isinstance(x, str) else True])
@FuncTools.attach_attr(docstring=doc.dcm_hierarchical_parser, info_func=True, entry_tp=Union[str, Any], return_tp=str)
def dcm_hierarchical_parser(**params):
    file, prefix = params.get('data'), '|---'

    regex = re.compile('^[A-Z]')
    keywords, res = [], []

    def expand_all(f, pre):

        f = _f_head(f) if isinstance(f, str) else f[0] if isinstance(f, list) and len(f) == 1 else f
        f.__str__()  # load f in memory if f is a pointer

        if hasattr(f, '_list'):
            for _sub in f:
                expand_all(f=_sub, pre=pre)
        else:
            for k in dir(f):
                if regex.search(k):  # matched pattern
                    _f = f.get_item(k)

                    res.append(pre+' '+k)
                    keywords.append(k)  # no remove duplicated items, for parallel tags

                    if getattr(_f, 'VR') == 'SQ':  # Sequence, sub structure exists
                        for __f in _f:
                            expand_all(f=__f, pre='| ' + pre)

    expand_all(f=file, pre=prefix)
    print(_return := '\n'.join(res))
    return _return


@FuncTools.params_setting(data=T[Null: lambda x: os.path.exists(x) if isinstance(x, str) else True],
                          attr_path=T[Null: Union[str, list[str], tuple[list[str], ...]]])
@FuncTools.attach_attr(docstring=doc.dcm_attr_loader, info_func=True, entry_tp=Union[str, Any],
                       return_tp=Union[Any, list[Any], tuple[list[Any], ...]])
def dcm_attr_loader(**params):
    _data, _path = params.get('data'), params.get('attr_path')
    _path = copy.deepcopy(_path) if isinstance(_path, (tuple, list)) else _path
    data = _f_head(_data) if isinstance(_data, str) else _data
    return tuple(_f_attr(data, _) for _ in _path) if isinstance(_path, tuple) else _f_attr(data, _path)


class DcmSetConstructor:

    @FuncTools.params_setting(data=T[Null: Iterable[str]], loader=T['SimpleITK': Literal['pydicom', 'SimpleITK']],
                              series_k=T["0020|000e": str], instance_k=T["0008|0018": str],
                              image_orientation_k=T["0020|0037": str], pixel_spacing_k=T["0028|0030": str],
                              image_position_k=T["0020|0032": str], spacing_between_slices_k=T["0018|0088": str],
                              **{'~stacking_axis': T[2: int], '~verbosity': T[False: bool],
                                 '~user_defined_io': T[None: Optional[Callable[[str], Any]]]})
    def __init__(self, **params):
        self.files = [_ for _ in params.pop('data')]
        self.series_k, self.instance_k = params.get('series_k'), params.get('instance_k')
        self.stacking_axis = params.get('~stacking_axis')

        # data load method setting
        self.loader = _DcmLoader(params.get('loader'))
        f_read, f_data, f_attr = (self.loader.robust_header_loader, self.loader.ndarray_image_loader,
                                  self.loader.attribute_loader)
        _inflow = default_param(params, '~user_defined_io', f_read)

        # loading-io, time consumption step; self.headers must be List[headers]
        print('loading dicom dataset...') if params.get('~verbosity') else ...
        self.headers = [_ for _ in io.generic_filter(data=self.files, filter_pattern=r'.*',
                                                     apply_map=lambda x: _inflow(x))]
        print('dataset loading completed.') if params.get('~verbosity') else ...

        if 'err_tag' in tuple(self.headers):  # logic for files without header
            err_file = [self.files[_] for _ in np.where(self.headers == 'err_tag')[0]]
            raise IOError(f'invalid file(s) {err_file} exists during data loading...')
        header_idx = np.unique([f_attr(item, self.instance_k) for item in self.headers], return_index=True)[1]
        self.headers, self.files = [[self.headers[_] for _ in header_idx], [self.files[_] for _ in header_idx]]
        set_ = np.array([f_attr(item, self.series_k) for item in self.headers])
        set_uni = np.unique(set_)

        idx_uni = [np.where(set_ == item)[0] for item in set_uni]
        self.dcm_set = [[self.headers[_] for _ in idx] for idx in idx_uni]
        self.files_set = [[self.files[_] for _ in idx] for idx in idx_uni]  # TODO: accelerate loading possibly

        if repr(self.stacking_axis) != 'None':  # code block for resort slices
            att, ax = params.get('image_position_k'), self.stacking_axis
            _ = [np.array([f_attr(item, att)[ax] for item in dcm]) for dcm in self.dcm_set]
            self.dcm_set = [[item[_1] for _1 in np.argsort(_id)] for _id, item in zip(_, self.dcm_set)]
            self.files_set = [[item[_1] for _1 in np.argsort(_id)] for _id, item in zip(_, self.files_set)]


class DcmSeries:

    @FuncTools.params_setting(data=T[Null: Iterable], loader=T['SimpleITK': Literal['pydicom', 'SimpleITK']],
                              series_k=T["0020|000e": str], instance_k=T["0008|0018": str],
                              image_orientation_k=T["0020|0037": str], pixel_spacing_k=T["0028|0030": str],
                              image_position_k=T["0020|0032": str], spacing_between_slices_k=T["0018|0088": str],
                              axis_order=T['zyx': Literal['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']],
                              template_meta=T[None: Optional[Any]],
                              roi_seq_map=T[None: Optional[Callable[[...], ndarray]]],  # value of FileDataset, maybe
                              roi_name_map=T[None: Optional[Callable[[str], ndarray]]],
                              **{'~is_sorted': T[True: bool], '~stacking_axis': T[2: int],
                                 '~verbosity': T[False: bool]})
    def __init__(self, **params):
        self.settings = {k: v for k, v in params.items() if k not in ['data']}
        self.data = params.get('data')
        self.stacking_axis = params.get('~stacking_axis')
        self.loader = _DcmLoader(params.get('loader'))
        if len(self.data) >= 1:  # not empty
            self.template: Any = self.data[0]
            self.template_meta = params.get('template_meta')
        self.affine = self.affine_matrix if hasattr(self, 'template') else np.zeros((4, 4))
        self.z_pos = np.where(np.array(self._intrinsic_order) == self.stacking_axis)[0][0]
        f_roi_seq = SingleMap({_roi_seq_to_ndarray: {'__data_key': 'ContourData',
                                                     '__coord': self.rcs_coordinate,
                                                     '__order': self._intrinsic_order,
                                                     '__z_pos': self.z_pos}})
        self.roi_seq_map = default_param(params, 'roi_seq_map', f_roi_seq)
        self.roi_name_map = default_param(params, 'roi_name_map',
                                          partial(_warn, msg='roi_name_map is available after link_struct execution'))
        self.dose, self.rcs_dose = None, None
        self.dvh_name_map = default_param(params, 'dvh_name_map',
                                          partial(_warn, msg='dvh_name_map is available after link_dose execution'))

    @property
    def metas(self):
        res = {}
        if hasattr(self, 'template'):
            f_keys, f_attr = self.loader.all_keys, self.loader.attribute_loader
            res.update(**{k: f_attr(self.template, k) for k in f_keys(self.template) if
                          len(np.unique([f_attr(self.data[_], k).__str__() for _ in range(len(self.data))])) == 1})
            if self.settings.get('spacing_between_slices_k') not in f_keys(self.template):
                res.update(**{self.settings.get('spacing_between_slices_k'):
                              np.linalg.norm(self.affine.T[:3], axis=1, ord=2)[self.stacking_axis]})
        return res

    @property
    def affine_matrix(self):

        if hasattr(self, 'template'):

            _no_stacking_axis_spacing, _no_sorted = False, False

            f_keys, f_attr = self.loader.all_keys, self.loader.attribute_loader

            xy_xyz = np.array(f_attr(self.template, self.settings.get('image_orientation_k')))
            assert_info_raiser(np.dot(*xy_xyz.reshape((2, 3))).__abs__() < 1e-4,
                               ValueError('no orthogonality system has been detected...'))  # ~orthogonality checking

            delta_ij = np.array(f_attr(self.template, self.settings.get('pixel_spacing_k')))
            plan_vec = xy_xyz.reshape((2, 3)) * np.repeat(delta_ij, 3).reshape((2, 3))

            # noinspection PyUnreachableCode
            _ = np.cross(plan_vec[0], plan_vec[1])
            _z = _/np.linalg.norm(_, ord=2)  # normal unit vector of plan

            norm_vec = np.array([0, 0, 0])
            if self.settings.get('spacing_between_slices_k') in f_keys(self.template):  # "0018|0088" existed
                norm_vec = f_attr(self.template, self.settings.get('spacing_between_slices_k')) * _z
            else:
                _no_stacking_axis_spacing = True

            if self.settings.get('~is_sorted'):
                s_xyz = np.array(f_attr(self.template, self.settings.get('image_position_k')))
            else:
                s_xyz = np.array(f_attr(self.template, self.settings.get('image_position_k')))[:2]
                _no_sorted = True

            if _no_stacking_axis_spacing or _no_sorted:  # for scale of norm_vec or s_xyz[-1]
                att, ax = self.settings.get('image_position_k'), self.settings.get('~stacking_axis')  # ~orthogonality
                norm_pos = np.array([f_attr(item, att)[ax] for item in self.data])
                idx = np.argsort(norm_pos)
                norm_pos_sorted = norm_pos[idx]

                if _no_stacking_axis_spacing:
                    norm_scale = np.diff(norm_pos_sorted)[0].__abs__() if len(norm_pos_sorted) > 1 else 0
                    norm_vec = _z * norm_scale

                if _no_sorted:
                    s_xyz = np.append(s_xyz, norm_pos_sorted[0])
                    self.data = [self.data[_] for _ in idx]  # resort step

            res = np.vstack((plan_vec, norm_vec, s_xyz)).T
            res = np.vstack((res, np.array([0, 0, 0, 1])))

        else:
            res = np.eye(4)

        return res

    @cached_property
    def _intrinsic_order(self):
        return _intrinsic_order(self.settings)

    @property
    def rcs_spacing(self):
        return _rcs_spacing(self.affine, self._intrinsic_order)

    @property
    def rcs_origin(self):
        return _rcs_origin(self.affine, self._intrinsic_order)

    @property
    def rcs_array(self):
        f_data = self.loader.ndarray_image_loader
        return np.dstack([f_data(item) for item in self.data]).transpose(self._intrinsic_order)

    @property
    def rcs_coordinate(self):
        return _rcs_coordinate(self.rcs_array, self.rcs_spacing, self.rcs_origin)

    @property
    def _suv_factor(self):
        err_info = 'required attributes are not satisfied when calculating SUV from PET modality'
        assert_info_raiser(hasattr(self, 'template_meta'), TypeError(err_info))
        requires, _attrs = (['RadiopharmaceuticalInformationSequence', 'AcquisitionTime', 'PatientWeight'],
                            self.template_meta.dir())
        assert_info_raiser(np.all([_ in _attrs for _ in requires]), TypeError(err_info))
        f, x = _f_attr, self.template_meta
        v1 = ['RadiopharmaceuticalInformationSequence', 'RadionuclideTotalDose']
        v2 = ['RadiopharmaceuticalInformationSequence', 'RadiopharmaceuticalStartTime']
        v3 = ['RadiopharmaceuticalInformationSequence', 'RadionuclideHalfLife']
        dose_t, t_s, life_h, t_acq, w = f(x, v1), f(x, v2), f(x, v3), f(x, requires[-2]), f(x, requires[-1])
        t_diff = _float_timestamp(t_acq) - _float_timestamp(t_s)
        return 1000 * w / (dose_t * 0.5 ** (t_diff / life_h))

    @property
    def rcs_suv(self):  # correction for PET modality
        try:
            a = self._suv_factor
        except TypeError as err:
            warnings.warn(f"SUV factor uses 1, due to {err}")
            a = 1
        return self.rcs_array * a

    @FuncTools.params_setting(data=T[Null: str], file_type=T[Null: Literal['dose', 'plan', 'struct']])
    def _link_obj(self, **params):
        obj, tp = params.get('data'), params.get('file_type')
        if tp == 'struct':
            self.struct = obj
        if tp == 'dose':
            self.dose = obj
        else:
            self.plan = obj

    @FuncTools.params_setting(data=T[Null: str], roi_name_k=T[None: Optional[Union[str, list[str]]]],
                              roi_numbrer_k=T[None: Optional[Union[str, list[str]]]],
                              contour_sequence_k=T[None: Optional[Union[str, list[str]]]],
                              referenced_roi_number_k=T[None: Optional[Union[str, list[str]]]],
                              roi_name_map=T[None: Optional[Callable[[str], ndarray]]])
    def link_struct(self, **params):
        roi_name = default_param(params, 'roi_name', ROIName)
        roi_number_k = default_param(params, 'roi_number_k', ROINumber)
        contour_sequence_k = default_param(params, 'contour_sequence_k', ContourSequence)
        referenced_roi_number_k = default_param(params, 'referenced_roi_number_k', ReferencedROINumber)
        self._link_obj(data=params.get('data'), file_type='struct')
        f_roi_name = SingleMap({_map_roi_from_names: {'struct_file': self.struct, 'roi_constructor': self.roi_seq_map,
                                                      'name_number_path': copy.deepcopy((roi_name, roi_number_k)),
                                                      'contour_number_path': copy.deepcopy((contour_sequence_k,
                                                                                            referenced_roi_number_k))}})
        self.roi_name_map = default_param(params, 'roi_name_map', f_roi_name)

    def _dose_affine(self, x, frame):
        f1, f_keys, f_attr = self.loader.robust_header_loader, self.loader.all_keys, self.loader.attribute_loader
        d_file = f1(x)
        xy_xyz = np.array(f_attr(d_file, self.settings.get('image_orientation_k')))
        assert_info_raiser(np.dot(*xy_xyz.reshape((2, 3))).__abs__() < 1e-4,
                           ValueError('no orthogonality system has been detected...'))  # ~orthogonality checking

        delta_ij = np.array(f_attr(d_file, self.settings.get('pixel_spacing_k')))
        plan_vec = xy_xyz.reshape((2, 3)) * np.repeat(delta_ij, 3).reshape((2, 3))

        # noinspection PyUnreachableCode
        _ = np.cross(plan_vec[0], plan_vec[1])
        _z = _ / np.linalg.norm(_, ord=2)  # normal unit vector of plan

        s_xyz = np.array(f_attr(d_file, self.settings.get('image_position_k')))
        f2 = (lambda x1, x2, : [a := np.array(f_attr(x1, frame)),
                                b := np.diff(a)[0].__abs__() if len(a) > 1 else 0, x2 * b][-1])
        _no_z_sp = False if self.settings.get('spacing_between_slices_k') in f_keys(d_file) else True
        norm_vec = f2(d_file, _z) if _no_z_sp else f_attr(d_file, self.settings.get('spacing_between_slices_k')) * _z
        res = np.vstack((plan_vec, norm_vec, s_xyz)).T
        res = np.vstack((res, np.array([0, 0, 0, 1])))
        return res

    def _dose_array(self, x, scale):
        f_head, f_array, f_attr = (self.loader.robust_header_loader, self.loader.ndarray_image_loader,
                                   self.loader.attribute_loader)
        hd = f_head(x)

        return f_array(hd).transpose((1, 2, 0)).transpose(self._intrinsic_order) * f_attr(hd, scale)

    def _rcs_dose(self, decomp_m, interp_m):
        _start, _end, _dose = self.dose.rcs_origin, np.array([_[-1] for _ in self.dose.rcs_coordinate]), self.dose
        start_, end_, sp_ = self.rcs_origin, np.array([_[-1] for _ in self.rcs_coordinate]), self.rcs_spacing
        st_dif, ed_dif = (np.array([v2-v1 for v1, v2 in zip(_start, start_)]),
                          np.array([v2-v1 for v1, v2 in zip(_end, end_)]))
        start, end = (np.array([max(v1, v2) for v1, v2 in zip(_start, start_)]),
                      np.array([min(v1, v2) for v1, v2 in zip(_end, end_)]))
        new_shape = tuple([int(np.ceil((v2 - v1) / v3)) for v1, v2, v3 in zip(start, end, sp_)])
        idx = tuple(slice(0 if v1 <= 0 else int(v1/sp1), k if v2 >= 0 else int(k+v2/sp1), 1)
                    for v1, v2, k, sp1 in zip(st_dif, ed_dif, _dose.rcs_array.shape, _dose.rcs_spacing))
        _dose_meta = _dose.rcs_array[idx]
        _meta = resize(data=_dose_meta, new_size=new_shape, decomp_method=decomp_m, interp_method=interp_m)
        _meta = np.pad(_meta, [np.array([0, expand]) for expand in
                               [v1 - v2 for v1, v2 in zip(self.rcs_array.shape, new_shape)]])
        _shift = tuple(int((v1-v2)/sp1) for v1, v2, sp1 in zip(start, start_, sp_))
        swap_pair = [s2 in 'xy' for s1, s2 in enumerate(self.settings.get('axis_order'))]
        _gen = (_ for _ in [v1 for v1, v2 in zip(_shift, swap_pair) if v2][::-1])
        _shift = tuple(v1 if not v2 else next(_gen) for v1, v2 in zip(_shift, swap_pair))  # swap x and y due dose_map
        return np.roll(_meta, shift=_shift, axis=[_ for _ in range(len(new_shape))])

    @FuncTools.params_setting(data=T[Null: str], grid_frame_offset_vector_k=T["3004|000c": Union[str, list[str]]],
                              dose_grid_scaling_k=T["3004|000e": Union[str, list[str]]],
                              decomp_method=T['tucker': Literal['cp', 'tucker']],
                              interp_method=T['linear': Literal['linear', 'nearest', 'nearest-up', 'zero', 'slinear',
                              'quadratic', 'cubic', 'previous', 'next']],
                              linspace_nums=T[100: int], dvh_name_map=T[None: Optional[Callable[[Union[list[str],
                              dict[str, ndarray]]], list[tuple[ndarray, ndarray]]]]])
    def link_dose(self, **params):
        """
        -> obj.dose (obj.dose.affine, obj.dose.rcs_array) -> obj.rcs_dose -> obj.dvh_name_map
        """
        dose_path = params.get('data')
        self._link_obj(data=dose_path, file_type='dose')
        self.dose = _Dose(affine=self._dose_affine(dose_path, params.get('grid_frame_offset_vector_k')),
                          rcs_array=self._dose_array(dose_path, params.get('dose_grid_scaling_k')),
                          axis_order=self._intrinsic_order)
        self.rcs_dose = self._rcs_dose(params.get('decomp_method'), params.get('interp_method'))
        f_dvh_name = SingleMap({_dvh_name_map: {'__dose': self.rcs_dose, '__msk_trans': self.roi_name_map,
                                                '__seps': params.get('linspace_nums')}})
        self.dvh_name_map = default_param(params, 'dvh_name_map', f_dvh_name)

    def link_plan(self, **params):
        self._link_obj(data=params.get('data'), file_type='plan')
        raise NotImplementedError


@FuncTools.params_setting(data=T[Null: Iterable[str]], loader=T['SimpleITK': Literal['pydicom', 'SimpleITK']],
                          series_k=T["0020|000e": str], instance_k=T["0008|0018": str],
                          image_orientation_k=T["0020|0037": str], pixel_spacing_k=T["0028|0030": str],
                          image_position_k=T["0020|0032": str], spacing_between_slices_k=T["0018|0088": str],
                          axis_order=T['zyx': Literal['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']],
                          **{'~use_template_meta': T[False: bool],
                             '~user_defined_io': T[None: Optional[Callable[[str], Any]]]})
@FuncTools.attach_attr(docstring=doc.dcm_constructor, info_func=True, entry_tp=Iterable[str], return_tp=list[DcmSeries],
                       **{'~unknown_tp': [DcmSeries]})
def dcm_constructor(**params):
    _, f = DcmSetConstructor(**params), _f_head  # SimpleITK_config for default
    settings = {k: v for k, v in params.items() if k not in ['data', 'template_meta']}
    if params.get('~use_template_meta'):  # forced save meta of 1st slice using pydicom, for each set
        return [DcmSeries(data=v2, template_meta=f(v1[0]), **settings) for v1, v2 in zip(_.files_set, _.dcm_set)]
    else:
        return [DcmSeries(data=v, template_meta=None, **settings) for v in _.dcm_set]


@FuncTools.params_setting(data=T[Null: Generator], regroup_reference=T[Null: list[str]],
                          loader=T['SimpleITK': Literal['SimpleITK', 'pydicom']],
                          rearrange=T[True: bool], dump_as=T['_regroup_refs': str],
                          **{'~verbosity': T[False: bool], '~user_defined_io': T[None: Optional[Callable[[str], Any]]]})
@FuncTools.attach_attr(docstring=doc.dcm_regroup, info_func=True, entry_tp=Generator, return_tp=dict)
def dcm_regroup(**params):
    entry_point, loader = params.get('data'), _DcmLoader(loader=params.get('loader'))
    header: dict = {'loader': loader.loader, 'regroup_reference': params.get('regroup_reference'),
                    'rearrange': params.get('rearrange'), 'dump_as': params.get('dump_as'), 'regroup_result': {}}
    res: dict = header['regroup_result']
    _load, _get = loader.robust_header_loader, loader.attribute_loader
    _load = default_param(params, '~user_defined_io', _load)
    _cons = [__cons] if not isinstance(__cons := params.get('regroup_reference'), list) else __cons
    _config_meta = eval(header.get('loader') + '_config') if header.get('rearrange') else dict()
    _config_meta.update({k: v for k, v in params.items() if k not in ['data', 'regroup_reference', 'loader',
                                                                      'rearrange', 'dump_as']})
    _is_prompt = params.get('~verbosity')

    def _build_regrouping_res(x: dict, path: list[str], _in_root: Iterable = None):  # x: to be modified obj
        k_outer, in_deepest = path[0], len(path) == 1

        if in_deepest:
            for _ in _in_root:
                hd = _load(_)
                tag = _get(hd, k_outer)
                if tag not in x.keys():
                    x.update({tag: []})
                x[tag].append(_)

            if _config_meta:  # rearrange code block
                for k, _v in x.items():
                    print(f'now processing case {k}...') if _is_prompt else ...
                    x[k] = DcmSetConstructor(data=_v, **_config_meta).files_set

        else:
            _files = np.array([_ for _ in _in_root])
            _cache = np.array([_get(_load(_), k_outer) for _ in _files])
            x_cp = {k: _files[np.where(_cache == k)] for k in np.unique(_cache)}
            x.update({k: dict() for k in x_cp.keys()})

            for _k, _v in x.items():
                _build_regrouping_res(x[_k], path[1:], x_cp[_k])

    _build_regrouping_res(res, _cons, entry_point)

    if f := params.get('dump_as'):
        _save(data=header, to_file=f)

    return header


def _refactor_meta(k: str, x: str):
    if x:  # not empty
        res = x
        if k not in ['ITK_FileNotes', 'ITK_original_direction', 'ITK_original_spacing', 'sform_code_name', 'qto_xyz',
                     'qform_code_name', 'qfac', 'aux_file', 'descrip']:
            res = [float(_) for _ in x.split(' ')] if x != 'NO' else ''
            res = res[0] if len(res) == 1 else res
    else:
        res = ''
    return res


def _metas(x: Image, f: Callable):
    return {k: f(k, x.GetMetaData(k)) for k in x.GetMetaDataKeys()}


def _affine_matrix(x: dict):
    """
    for reference:
    https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/qsform.html
    """
    if x.get('sform_code') > 0:  # meth 3
        res = np.array([v for k, v in x.items() if k in ['srow_x', 'srow_y', 'srow_z']] + [[0, 0, 0, 1]])
    else:  # meth 1 or 2
        qform_code, qfac = x.get('qform_code'), x.get('qfac')

        try:
            assert qform_code > 0 and qfac in ['1', '-1']  # support old criterion, qform_code = 0
        except AssertionError as _:  # meth 1
            from warnings import warn
            warn(f'no sufficient to construct rotation matrix, direction uses\n{np.eye(3)} instead')
            _res = np.vstack([np.hstack([np.diag([x.get(f'pixdim[{_}]') for _ in '123']),
                                         np.array([x.get(f'qoffset_{_}') for _ in 'xyz'])[..., np.newaxis]]),
                              np.array([0, 0, 0, 1])[..., np.newaxis].T])
        else:  # meth 2
            r_mat = np.diag([x.get(f'pixdim[{_}]') for _ in '123'])
            r_mat[2] = float(qfac) * r_mat[2]
            _res = np.vstack([np.hstack([r_mat, np.array([x.get(f'qoffset_{_}') for _ in 'xyz'])[..., np.newaxis]]),
                              np.array([0, 0, 0, 1])[..., np.newaxis].T])
        res = _res
    return res


class NIfTI:

    @FuncTools.params_setting(data=T[Null: lambda x: os.path.exists(x)])
    def __init__(self, **params):
        self.settings = {k: v for k, v in params.items() if k in ['preprocess_meta', 'axis_order']}
        self._obj = Itk.ReadImage(params.get('data'), imageIO='NiftiImageIO')
        self.affine = self.affine_matrix

    @property
    def metas(self):
        return _metas(self._obj, self.settings.get('preprocess_meta'))

    @property
    def affine_matrix(self):
        return _affine_matrix(self.metas)

    @cached_property
    def _intrinsic_order(self):
        return _intrinsic_order(self.settings)

    @property
    def rcs_spacing(self):
        return _rcs_spacing(self.affine, self._intrinsic_order)

    @property
    def rcs_origin(self):
        return _rcs_origin(self.affine, self._intrinsic_order)

    @property
    def rcs_array(self):
        return _rcs_array(self._obj, self._intrinsic_order)

    @property
    def rcs_coordinate(self):
        return _rcs_coordinate(self.rcs_array, self.rcs_spacing, self.rcs_origin)


@FuncTools.params_setting(data=T[Null: Union[str, Iterable[str]]],
                          preprocess_meta=T[_refactor_meta: Callable[[str, str], Union[str, Numeric, list[Numeric]]]],
                          axis_order=T['zyx': Literal['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']],
                          **{'~user_defined_io': T[None: Optional[Callable[[str], Any]]]})
@FuncTools.attach_attr(docstring=doc.nii_constructor, info_func=True, entry_tp=Union[str, Iterable[str]],
                       return_tp=Union[NIfTI, list[NIfTI]], **{'~unknown_tp': [NIfTI]})
def nii_constructor(**params):
    f = default_param(params, '~user_defined_io', NIfTI)
    return (f(**params) if isinstance(params.get('data'), str) else [_conf := {k: v for k, v in params.items()
            if k not in ['data']}, [f(data=_, **_conf) for _ in params.get('data')]][-1])


doc.redoc(DcmSetConstructor, doc.DcmSetConstructor)
doc.redoc(DcmSeries, doc.DcmSeries)
doc.redoc(NIfTI, doc.NIfTI)


__all__ = ['DcmSetConstructor', 'DcmSeries', 'struct_config', 'pydicom_config', 'SimpleITK_config', 'dcm_constructor',
           'dcm_hierarchical_parser', 'dcm_attr_loader', 'dcm_regroup', 'ROIName', 'ROINumber', 'ContourSequence',
           'ReferencedROINumber', 'NIfTI', 'nii_constructor']


if __name__ == '__main__':
    pass
