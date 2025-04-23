from info.basic.core import Unit, ExeDict
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null
from typing import Optional, Any
import info.docfunc as doc


@FuncTools.params_setting(data=T[Null: Any], o_prt=T[None: Optional[ExeDict]], o_sav=T[None: Optional[ExeDict]],
                          o_vis=T[None: Optional[ExeDict]], **{'~unknown_tp': [ExeDict]})
@FuncTools.attach_attr(docstring=doc.operations, info_func=True, entry_tp=Any, return_tp=Any)
def operations(**params):
    dt = params.get('data')

    if not params.get('o_prt') is None:  # logic for printing
        src: ExeDict = params.get('o_prt')
        src(data=dt)

    if not params.get('o_sav') is None:  # logic for saving
        src: ExeDict = params.get('o_sav')
        src(data=dt)

    if not params.get('o_vis') is None:  # logic for visualization
        src: ExeDict = params.get('o_vis')
        src(data=dt)

    return dt


operations_u = Unit(mappings=[operations])
printing_u: Unit = operations_u.shadow(o_sav=None,  o_vis=None, docstring=doc.printing_u)
saving_u: Unit = operations_u.shadow(o_prt=None, o_vis=None, docstring=doc.saving_u)
visual_u: Unit = operations_u.shadow(o_prt=None, o_sav=None, docstring=doc.visual_u)


__all__ = ['operations', 'operations_u', 'printing_u', 'saving_u', 'visual_u']


if __name__ == '__main__':
    pass
