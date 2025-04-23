from info.basic.functions import files_searcher
from info.basic.decorators import FuncTools
from info.basic.core import ExeDict
from info.basic.typehint import T, Null
from info.toolbox.libs.operations.generic import operations
import info.docfunc as doc
from typing import Optional, Union, Any, NoReturn, Callable
from functools import partial
import logging
import zipfile
import os


funcs = __import__('info.basic.functions', fromlist=['_save'])
_save = getattr(funcs, '_save')
_append_suffix = getattr(funcs, '_append_suffix')


@FuncTools.params_setting(data=T[Null: object], to_file=T[Null: Union[str, list[str]]],
                          compress_in=T[None: Optional[str]])
@FuncTools.attach_attr(docstring=doc.archive, info_func=True, entry_tp=Any, return_tp=NoReturn)
def archive(**params):
    dt, to_file = params.get('data'), params.get('to_file')
    to_file = [to_file] if isinstance(to_file, str) else to_file  # one str only
    to_file = _append_suffix(to_file) if isinstance(to_file[0], str) else to_file

    if len(to_file) == 1:
        _save(data=dt, to_file=to_file[0])
    else:
        for k, v in zip(to_file, dt):
            _save(data=v, to_file=k)

    if into := params.get('compress_in'):
        _save(data=to_file, to_file='_header.pyp')
        to_file.append('_header.pyp')
        z_algo, z_level = params.get('~compress_algorithm', 8), params.get('~compress_level', 5)

        into = into if len(into) > 7 and into[-7:] == '.pyp.gz' else into + '.pyp.gz'
        with zipfile.ZipFile(into, 'w', allowZip64=True, compression=z_algo, compresslevel=z_level,
                             strict_timestamps=False) as f1:
            for f2 in to_file:
                f1.write(f2)

        for f3 in files_searcher('.', lambda x: x[-3:] == 'pyp'):
            os.remove(f3)


@FuncTools.params_setting(data=T[Null: object], extractors=T[{}: dict[str, Callable[[Any], str]]],
                          directory=T[os.getcwd(): str], to_file=T['.df_sav': str], other_params=T[{}: dict])
@FuncTools.attach_attr(docstring=doc.generic_logger, info_func=True, entry_tp=Any, return_tp=NoReturn)
def generic_logger(**params):

    # Note: all feature extract functions in extractors will be executed as func(data=..., **other_params)
    log_name = params.pop('to_file')
    features_funcs: dict = params.pop('extractors')
    body: dict = params.pop('other_params')
    body.update(data=params.pop('data'))
    cols, vals = [], []

    for features, func in features_funcs.items():

        _ = func(**body)

        if not hasattr(_, '__iter__') or isinstance(_, str):
            cols.append(features)
            vals.append(_)
        else:
            count = 0
            for val in _.__iter__():
                cols.append(features + '_{}'.format(str(count)))
                vals.append(val)
                count += 1

    path_file = os.path.sep.join((params.get('directory'), log_name))

    logger, handler = logging.getLogger(log_name), logging.FileHandler(path_file)
    handler.setFormatter(logging.Formatter(fmt='%(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    if os.path.exists(path_file):

        if os.stat(path_file)[6] == 0:  # init column names
            logger.info(';'.join(cols))

        else:  # not empty file
            with open(path_file, 'r') as f:
                _ = f.readline()
            _new = ';'.join(cols) + '\n'  # first line of existed file

            if len(_) != len(_new) or not all([i == j for i, j in zip(_, _new)]):  # not same columns
                raise IOError('file {} consists of columns {}, but now attempt to write '
                              '{}'.format(params.get('to_file', '.df_sav'), _, _new))

    logger.info(';'.join([str(_) for _ in vals]))
    logger.handlers.pop()  # reset handlers


@FuncTools.params_setting(data=T[Null: tuple[Any, Exception]], directory=T[os.getcwd(): str],
                          to_file=T['run_error.log': str])
@FuncTools.attach_attr(docstring=doc.exception_logger, info_func=True, entry_tp=tuple[Any, Exception], return_tp=str)
def exception_logger(**params):
    case, err = params.get('data')
    _case_name = (lambda **_: _.get('data'))
    _err_type = (lambda **_: str(type(err)))
    _err_info = (lambda **_: err.__str__())
    sav = partial(operations, o_sav=ExeDict(execute=generic_logger,
                                            extractors={'case': _case_name,
                                                        'err_type': _err_type,
                                                        'err_info': _err_info},
                                            directory=params.get('directory'),
                                            to_file=params.get('to_file')))
    return sav(data=case)


__all__ = ['archive', 'generic_logger', 'exception_logger']


if __name__ == '__main__':
    pass
