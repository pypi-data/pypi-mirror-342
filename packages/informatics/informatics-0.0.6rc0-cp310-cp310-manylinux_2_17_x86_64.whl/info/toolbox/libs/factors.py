from info.basic.functions import default_param
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null, Numeric
from typing import Any, Callable, Optional
from info.toolbox.libs.hypotest import hypoi_sw, hypoi_f
from info import docfunc as doc
from numpy import ndarray
import numpy as np
from pandas import DataFrame
from functools import partial
from warnings import warn


_warn_msg = 'repeats less than 3, use mean instead, for statistic might not be accurate...'
func = __import__('info.basic.functions', fromlist=['_real_projection'])
_real_projection = getattr(func, '_real_projection')
_decomp_facs = getattr(func, '_decomp_facs')
_num_facs = getattr(func, '_num_facs')
_tenser_var = getattr(func, '_tenser_var')
_ranges = getattr(func, '_ranges')
_normality = (lambda x, emp=np.nan: [emp if len(x) == 0 else [warn(_warn_msg), np.mean(x)+0j][-1] if len(x) < 3 else
                                     [_ := hypoi_sw(data={'': np.array(x)}), sp := list(_.values()),
                                      mod_v := (np.linalg.norm([sp[0], 1-sp[1]], ord=2), np.mean(x)),
                                      comp := (mod_v[1]*(sp[0]/mod_v[0]), mod_v[1]*((1-sp[1])/mod_v[0])),
                                      comp[0] + comp[1]*1j][-1]][-1])
_anova = (lambda x, emp=np.nan: [x := [_ for _ in x], _ref := [[v2 for v2 in v1] for v1 in x if len(v1) >= 0],
                                 res := hypoi_f(data={f'{n}': np.array(v) for n, v in enumerate(_ref)}),
                                 p := res.get('F_pvalue'), np.log10(1/p) if p else emp][-1])
_default_agg = (lambda x, emp=np.nan: _anova([_real_projection([_normality([v3 for v3 in v2], emp) for v2 in v1], emp)
                                              for v1 in x], emp))


@FuncTools.params_setting(data=T[Null: DataFrame], constructor=T[Null: dict[str, list[str]]],
                          response_dimensions=T[Null: list[str]], inertia_dimensions=T[None: Optional[list[str]]],
                          measure=T[None: Optional[Callable[[list[list[list[Numeric]]]], Numeric]]],
                          empty_value=T[np.nan: Any], score_output=T[False: bool])
@FuncTools.attach_attr(docstring=doc.priori_scoring, info_func=True, entry_tp=DataFrame, return_tp=dict[str, ndarray])
def priori_scoring(**params):
    df, cons, dim_res = params.get('data'), params.get('constructor'), params.get('response_dimensions')
    rows, columns, data = df.index.values, df.columns.values, df.values
    ref, keys_pos = _decomp_facs(rows, cons), {kv[0]: idx for idx, kv in enumerate(cons.items())}
    keys, lvs, alpha = list(keys_pos.keys()), list(np.max(ref, axis=0)+1), params.get('alpha')
    dim_ine = default_param(params, 'inertia_dimensions', [_ for _ in keys if _ not in dim_res])
    num_ine, num_res, emp_v = _num_facs(dim_ine, lvs, keys), _num_facs(dim_res, lvs, keys), params.get('empty_value')
    f_agg = default_param(params, 'measure', partial(_default_agg, emp=emp_v))
    sc = [f_agg(_tenser_var(ref, _, keys_pos, dim_res, dim_ine, (num_ine, num_res))) for _ in data.T]
    sc = np.array([0.0 if not _ >= 0 else _ for _ in sc])  # modify nan to 0.0
    sc_levels = _ranges(int(np.ceil(0.1*np.max(sc))))
    _pos = {f'importance_level_{_idx}': np.where((s1 < sc) & (sc <= s2)) for _idx, (s1, s2) in enumerate(sc_levels)}
    _pos.update({'importance_level_redundance': np.where(sc == 0.0)})
    return {k: np.array([columns[v], sc[v]]).T if params.get('score_output') else columns[v] for k, v in _pos.items()}


__all__ = ['priori_scoring']


if __name__ == '__main__':
    pass
