from info.basic.functions import files_searcher, hdfs_searcher, hdfs_leaf_folder
from info.basic.functions import leaf_folder as _leaf_folder
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null
import info.docfunc as doc
from typing import Optional, Callable, Iterable, Union, Generator, Any, Literal
import numpy as np
import dill
import zipfile
import re


Unit = __import__('info.basic.core', fromlist=['Unit']).Unit
_load = getattr(__import__('info.basic.functions', fromlist=['_load']), '_load')


@FuncTools.params_setting(data=T[Null: str], file_system=T['desktop': Literal['desktop', 'hdfs']])
@FuncTools.attach_attr(docstring=doc.leaf_folders, info_func=True, entry_tp=str, return_tp=Generator)
def leaf_folders(**params):
    root, f_sys = params.get('data'), params.get('file_system')
    return _leaf_folder(root) if f_sys == 'desktop' else hdfs_leaf_folder(root)


@FuncTools.params_setting(data=T[Null: str], search_condition=T[lambda x: x: Callable[[Any], str]],
                          file_system=T['desktop': Literal['desktop', 'hdfs']])
@FuncTools.attach_attr(docstring=doc.search_from_root, info_func=True, entry_tp=str, return_tp=Generator)
def search_from_root(**params):
    root, cond, f_sys = params.get('data'), params.get('search_condition'), params.get('file_system')
    return files_searcher(root, cond) if f_sys == 'desktop' else hdfs_searcher(root, cond)


@FuncTools.params_setting(data=T[Null: Iterable], filter_pattern=T[r'.*': str], apply_map=T[None: Optional[Callable]])
@FuncTools.attach_attr(docstring=doc.generic_filter, info_func=True, entry_tp=Iterable, return_tp=Generator)
def generic_filter(**params):
    dt, regex, mp = params.get('data'), re.compile(params.get('filter_pattern')), params.get('apply_map')
    for item in dt:
        if regex.search(item):
            yield mp(item) if mp else item


@FuncTools.params_setting(data=T[Null: Iterable], regroup_labels=T[[r'.*']: list[str]])
@FuncTools.attach_attr(docstring=doc.files_regroup, info_func=True, entry_tp=Iterable, return_tp=dict[str, Iterable])
def files_regroup(**params):
    files, regroup_labels = (np.array(tuple(params.get('data'))), params.get('regroup_labels'))
    regex_lst = [re.compile(rf"{tag}") for tag in regroup_labels]
    search_res = [[reg.search(file) for file in files] for reg in regex_lst]
    res_ = [files[np.where(np.array(search_res[_]))] for _ in range(len(regroup_labels))]
    return {regroup_labels[_]: res_[_] for _ in range(len(regroup_labels))}


@FuncTools.params_setting(data=T[Null: dict[str, Iterable]], match_pattern=T[r'.*': str],
                          using_map=T[None: Optional[Callable]])
@FuncTools.attach_attr(docstring=doc.dict_filter, info_func=True, entry_tp=dict[str, Iterable],
                       return_tp=dict[str, Iterable])
def dict_filter(**params):
    grp_dict, regex, mp = params.get('data'), rf"{params.get('match_pattern')}", params.get('using_map')
    return {k: np.array(list(generic_filter(data=v, filter_pattern=regex, apply_map=mp)), dtype=object)
            for k, v in grp_dict.items()}


@FuncTools.params_setting(data=T[Null: Union[str, list[str]]])
@FuncTools.attach_attr(docstring=doc.unarchive, info_func=True, entry_tp=Union[str, list[str]],
                       return_tp=Union[Generator, object])
def unarchive(**params):
    dt = params.get('data')

    def _gen_version(x: Union[list, str]):
        if isinstance(x, list):
            for f in x:
                yield _load(data=f)
        elif isinstance(x, str):
            z_algo, z_level = params.get('~compress_algorithm', 8), params.get('~compress_level', 5)
            with zipfile.ZipFile(x, 'r', allowZip64=True, compression=z_algo, compresslevel=z_level,
                                 strict_timestamps=False) as f1:
                _files = dill.loads(f1.read('_header.pyp'))
                for f2 in _files:
                    yield dill.loads(f1.read(f2))

    def _return_version(x: str):
        return _load(data=x)

    if isinstance(dt, str):
        if len(dt) <= 4 or (len(dt) > 4 and dt[-4:] != '.pyp'):
            dt = dt + '.pyp'

    if isinstance(dt, list) or (isinstance(dt, str) and len(dt) > 7 and dt[-7:] == '.pyp.gz'):
        return (_ for _ in _gen_version(dt))  # yield from _gen_version(dt)
    elif isinstance(dt, str) and len(dt) > 4 and dt[-4:] == '.pyp':
        return _return_version(dt)  # return data


__all__ = ['leaf_folders', 'search_from_root', 'generic_filter', 'files_regroup', 'dict_filter', 'unarchive']


if __name__ == '__main__':
    pass
