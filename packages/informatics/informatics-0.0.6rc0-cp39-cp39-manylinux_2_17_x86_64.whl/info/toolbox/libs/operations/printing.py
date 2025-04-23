from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null
from typing import Any, NoReturn
import info.docfunc as doc


@FuncTools.params_setting(data=T[Null: object], attrs=T[[]: list[str]])
@FuncTools.attach_attr(docstring=doc.generic_printer, info_func=True, entry_tp=Any, return_tp=NoReturn)
def generic_printer(**params):
    dt: object = params.get('data')
    assert issubclass(type(dt), object)  # highlighter, no use
    attrs: list = params.get('attrs')
    for idx, attr in enumerate(attrs):
        if idx == 0:
            print('| ', end='')
        print(attr, ': ', sep='', end='')
        exec(f"print(dt.{attr}, end=' | ')")
    print()  # init new line


__all__ = ['generic_printer']


if __name__ == '__main__':
    pass
