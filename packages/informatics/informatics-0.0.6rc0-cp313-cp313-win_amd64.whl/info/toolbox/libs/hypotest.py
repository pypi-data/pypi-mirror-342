from info.basic.functions import assert_info_raiser
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null, Numeric
from info import docfunc as doc
from typing import Union, Optional, Callable, Iterable, Literal
from scipy.stats import norm
from itertools import combinations
from functools import partial
from numpy import ndarray
import numpy as np


dist = __import__('scipy.stats._distn_infrastructure', fromlist=['rv_frozen']).rv_frozen
Unit = __import__('info.basic.core', fromlist=['Unit']).Unit
func = __import__('info.basic.functions', fromlist=['_to_distance_matrix'])
distance_matrix = getattr(func, 'distance_matrix')
var_name = getattr(func, 'var_name')
_ravel_all = getattr(func, '_ravel_all')
_is_all_vals_related = getattr(func, '_is_all_vals_related')
_is_all_mats_related = getattr(func, '_is_all_mats_related')
_has_no_nan = getattr(func, '_has_no_nan')
_dict_extra = getattr(func, '_dict_extra')


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]])
@FuncTools.attach_attr(docstring=doc.hypoi_f, info_func=True, entry_tp=dict[str, ndarray], return_tp=dict[str, Numeric])
def hypoi_f(**params):
    from scipy.stats import f_oneway
    s, p = f_oneway(*tuple(np.ravel(v) if v.ndim != 1 else v for k, v in params.get('data').items()))
    return {'F_statistic': s, 'F_pvalue': p}


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], equal_var=T[False: bool], trim=T[0.: float],
                          permutations=T[None: Optional[int]], random_state=T[None: Optional[int]],
                          nan_policy=T['propagate': Literal['propagate', 'raise', 'omit']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoi_t, info_func=True, entry_tp=dict[str, ndarray], return_tp=dict[str, Numeric])
def hypoi_t(**params):
    from scipy.stats import ttest_ind
    eq_var, trim, permutation, seed = (params.get('equal_var', False), params.get('trim'),
                                       params.get('permutations'), params.get('random_state'))
    policy, alter, data, res = params.get('nan_policy'), params.get('alternative'), params.get('data'), {}
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = ttest_ind(v1, v2, equal_var=eq_var, nan_policy=policy, permutations=permutation, random_state=seed,
                         alternative=alter, trim=trim)
        res.update({f'T_independent_({k1})*({k2})_statistic': s, f'T_independent_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]])
@FuncTools.attach_attr(docstring=doc.hypoi_sw, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_sw(**params):
    from scipy.stats import shapiro
    res = {}
    for k, v in params.get('data').items():
        s, p = shapiro(v)
        res.update({f'Shapiro_Wilk_({k})_statistic': s, f'Shapiro_Wilk_({k})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], nan_policy=T['omit': Literal['propagate', 'raise', 'omit']])
@FuncTools.attach_attr(docstring=doc.hypoi_normality, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_normality(**params):
    from scipy.stats import normaltest
    res = {}
    for k, v in params.get('data').items():
        s, p = normaltest(v, axis=None, nan_policy=params.get('nan_policy'))  # ravel for v.ndim > 1
        res.update({f'normality_({k})_statistic': s, f'normality_({k})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], dist=T[norm(loc=0, scale=1): Union[dist, list[dist]]],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']],
                          method=T['auto': Literal['auto', 'exact', 'asymp']], n_samples=T[20: int])
@FuncTools.attach_attr(docstring=doc.hypoi_ks, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, Numeric]]], **{'~unknown_tp': [dist]})
def hypoi_ks(**params):
    from scipy.stats import kstest
    data, _dis = params.get('data'), params.get('dist')
    alter, m, n = params.get('alternative'), params.get('method'), params.get('n_sample')
    res, dis_set, extra = {}, [_dis] if not hasattr(_dis, '__len__') else _dis, params.get('~full_return', False)
    for dis in dis_set:  # self hypothesis test:
        name = dis.dist.name
        for k, v in data.items():
            v = v if v.ndim == 1 else np.ravel(v)
            _ = kstest(v, dis.cdf, N=n, alternative=alter, method=m)
            res.update({f'Kolmogorov_Smirnov_({name})@({k})_statistic': _[0],
                        f'Kolmogorov_Smirnov_({name})@({k})_pvalue': _[1]})
            if extra:
                ex = _dict_extra(_, ['statistic_location', 'statistic_sign'])
                res.update({f'Kolmogorov_Smirnov_({name})@({k})_extra': ex})
    for k1, k2 in combinations(list(data.keys()), 2):  # pair-wise hypothesis test:
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        _ = kstest(v1, v2, alternative=alter, method=m)
        res.update({f'Kolmogorov_Smirnov_({k1})*({k2})_statistic': _[0],
                    f'Kolmogorov_Smirnov_({k1})*({k2})_pvalue': _[1]})
        if extra:
            ex = _dict_extra(_, ['statistic_location', 'statistic_sign'])
            res.update({f'Kolmogorov_Smirnov_({k1})*({k2})_extra': ex})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], dist=T[norm(loc=0, scale=1): Union[dist, list[dist]]],
                          method=T['auto': Literal['auto', 'asymp', 'exact']])
@FuncTools.attach_attr(docstring=doc.hypoi_cvm, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric], **{'~unknown_tp': [dist]})
def hypoi_cvm(**params):
    from scipy.stats import cramervonmises, cramervonmises_2samp
    data, _dis = params.get('data'), params.get('dist')
    res, dis_set, m = {}, [_dis] if not hasattr(_dis, '__len__') else _dis, params.get('method')
    m = 'asymptotic' if m == 'asymp' else m
    for dis in dis_set:  # self hypothesis test:
        name = dis.dist.name
        for k, v in data.items():
            v = v if v.ndim == 1 else np.ravel(v)
            _ = cramervonmises(v, dis.cdf)
            res.update({f'Cramér_Von_Mises_({name})@({k})_statistic': _.statistic,
                        f'Cramér_Von_Mises_({name})@({k})_pvalue': _.pvalue})
    for k1, k2 in combinations(list(data.keys()), 2):  # pair-wise hypothesis test:
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        _ = cramervonmises_2samp(v1, v2, method=m)
        res.update({f'Cramér_Von_Mises_({k1})*({k2})_statistic': _.statistic,
                    f'Cramér_Von_Mises_({k1})*({k2})_pvalue': _.pvalue})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']])
@FuncTools.attach_attr(docstring=doc.hypoi_ag, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_ag(**params):
    from scipy.stats import alexandergovern
    _ = alexandergovern(*tuple(np.ravel(v) if v.ndim != 1 else v for k, v in params.get('data').items()),
                        nan_policy=params.get('nan_policy'))
    s, p = _.statistic if hasattr(_, 'statistic') else np.nan, _.pvalue if hasattr(_, 'pvalue') else np.nan
    return {'Alexander_Govern_statistic': s, 'Alexander_Govern_pvalue': p}


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]])
@FuncTools.attach_attr(docstring=doc.hypoi_thsd, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, Numeric]]])
def hypoi_thsd(**params):
    from scipy.stats import tukey_hsd
    keys, vals = (lambda x: (tuple(x.keys()), _ravel_all(*tuple(x.values()))))(params.get('data'))
    _, res, extra = tukey_hsd(*vals), {}, params.get('~full_return', False)
    _statistic, _pvalue, _interval = _.statistic, _.pvalue, _.confidence_interval()
    for dual_keys, dual_idx in zip(combinations(keys, 2), combinations(tuple(_ for _ in range(len(keys))), 2)):
        res.update({f'Tucky_HSD_({dual_keys[0]})*({dual_keys[1]})_statistic': _statistic[dual_idx[0], dual_idx[1]],
                    f'Tucky_HSD_({dual_keys[0]})*({dual_keys[1]})_pvalue': _pvalue[dual_idx[0], dual_idx[1]]})
        if extra:
            res.update({f'Tucky_HSD_({dual_keys[0]})*({dual_keys[1]})_extra':
                        {'ci_low': _interval.low[dual_idx[0], dual_idx[1]],
                         'ci_high': _interval.high[dual_idx[0], dual_idx[1]]}})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']])
@FuncTools.attach_attr(docstring=doc.hypoi_kw, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_kw(**params):
    from scipy.stats import kruskal
    s, p = kruskal(*tuple(np.ravel(v) if v.ndim != 1 else v for k, v in params.get('data').items()),
                   nan_policy=params.get('nan_policy'))
    return {'Kruskal_Wallis_H_statistic': s, 'Kruskal_Wallis_H_pvalue': p}


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], ties=T['below': Literal['below', 'above', 'ignore']],
                          correction=T[True: bool], power_lambda=T[1.: float],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoi_mood, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, Union[Numeric, ndarray]]]])
def hypoi_mood(**params):
    from scipy.stats import median_test, mood
    data, ties, cor, exp, policy = (params.get('data'), params.get('ties'), params.get('correction'),
                                    params.get('power_lambda'), params.get('nan_policy'))
    res, alter, extra = {}, params.get('alternative'), params.get('~full_return', False)
    _ = median_test(*tuple(v if v.ndim == 1 else np.ravel(v) for _, v in data.items()), ties=ties,
                    correction=cor, lambda_=exp, nan_policy=policy)
    res.update({'Mood_Median_statistic': _[0], 'Mood_Median_pvalue': _[1]})
    if extra:
        res.update({'Mood_Median_extra': {'median': _[2], 'table': _[3]}})
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = mood(v1, v2, axis=0, alternative=alter)
        res.update({f'Mood_Scale_({k1})*({k2})_statistic': s, f'Mood_Scale_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]])
@FuncTools.attach_attr(docstring=doc.hypoi_bartlett, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_bartlett(**params):
    from scipy.stats import bartlett
    s, p = bartlett(*tuple(np.ravel(v) if v.ndim != 1 else v for k, v in params.get('data').items()))
    return {'Bartlett_statistic': s, 'Bartlett_pvalue': p}


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], center=T['median': Literal['mean', 'median', 'trimmed']],
                          proportiontocut=T[0.05: float])
@FuncTools.attach_attr(docstring=doc.hypoi_levene, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_levene(**params):
    from scipy.stats import levene
    s, p = levene(*tuple(np.ravel(v) if v.ndim != 1 else v for k, v in params.get('data').items()),
                  center=params.get('center'), proportiontocut=params.get('proportiontocut'))
    return {'Levene_statistic': s, 'Levene_pvalue': p}


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], center=T['median': Literal['mean', 'median', 'trimmed']],
                          proportiontocut=T[0.05: float])
@FuncTools.attach_attr(docstring=doc.hypoi_fk, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_fk(**params):
    from scipy.stats import fligner
    s, p = fligner(*tuple(np.ravel(v) if v.ndim != 1 else v for k, v in params.get('data').items()),
                   center=params.get('center'), proportiontocut=params.get('proportiontocut'))
    return {'Fligner_Killeen_statistic': s, 'Fligner-Killeen_pvalue': p}


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], midrank=T[True: bool])
@FuncTools.attach_attr(docstring=doc.hypoi_ad, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, ndarray]]])
def hypoi_ad(**params):
    from scipy.stats import anderson_ksamp
    data, rank, extra = params.get('data'), params.get('midrank'), params.get('~full_return', False)
    _ = anderson_ksamp(_ravel_all(*tuple(v for _, v in data.items())), rank)
    res = {'Anderson_Darling_statistic': _[0], 'Anderson_Darling_pvalue': _[-1]}
    if extra:
        res.update({'Anderson_Darling_extra': {'critical_values': _[1]}})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoi_rank, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_rank(**params):
    from scipy.stats import ranksums
    data, alter = params.get('data'), params.get('alternative')
    res = {}
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = ranksums(v1, v2, alter)
        res.update({f'Wilcoxon_Ranksum_({k1})*({k2})_statistic': s, f'Wilcoxon_Ranksum_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], es_t=T[(.4, .8): tuple[float, float]])
@FuncTools.attach_attr(docstring=doc.hypoi_es, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_es(**params):
    from scipy.stats import epps_singleton_2samp
    data, res, t = params.get('data'), {}, params.get('es_t')
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = epps_singleton_2samp(v1, v2, t) if _has_no_nan(v1, v2) else (np.nan, np.nan)
        res.update({f'Epps_Singleton_({k1})*({k2})_statistic': s, f'Epps_Singleton_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], method=T['auto': Literal['auto', 'asymptotic', 'exact']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']],
                          u_continuity=T[True: bool])
@FuncTools.attach_attr(docstring=doc.hypoi_u, info_func=True, entry_tp=dict[str, ndarray], return_tp=dict[str, Numeric])
def hypoi_u(**params):
    from scipy.stats import mannwhitneyu
    data, res, alter, m, _c = (params.get('data'), {}, params.get('alternative'), params.get('method'),
                               params.get('u_continuity'))
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = mannwhitneyu(v1, v2, use_continuity=_c, alternative=alter, method=m)
        res.update({f'Mann_Whitney_U_({k1})*({k2})_statistic': s, f'Mann_Whitney_U_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], bm_dis=T['t': Literal['t', 'normal']],
                          nan_policy=T['propagate': Literal['propagate', 'raise', 'omit']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoi_bm, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_bm(**params):
    from scipy.stats import brunnermunzel
    res, data, policy, alter, dis = ({}, params.get('data'), params.get('nan_policy'), params.get('alternative'),
                                     params.get('bm_dis'))
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = brunnermunzel(v1, v2, alternative=alter, distribution=dis, nan_policy=policy)
        res.update({f'Brunner_Munzel_({k1})*({k2})_statistic': s, f'Brunner_Munzel_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoi_ab, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_ab(**params):
    from scipy.stats import ansari
    data, alter, res = params.get('data'), params.get('alternative'), {}
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = ansari(v1, v2, alter)
        res.update({f'Ansari_Bradley_({k1})*({k2})_statistic': s, f'Ansari_Bradley_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoi_skew, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_skew(**params):
    from scipy.stats import skewtest
    res, policy, alter = {}, params.get('nan_policy'), params.get('alternative')
    for k, v in params.get('data').items():
        v = np.ravel(v) if v.ndim > 1 else v
        s, p = skewtest(v, nan_policy=policy, alternative=alter)
        res.update({f'Skewness_({k})_statistic': s, f'Skewness_({k})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoi_kurtosis, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_kurtosis(**params):
    from scipy.stats import kurtosistest
    res, policy, alter = {}, params.get('nan_policy'), params.get('alternative')
    for k, v in params.get('data').items():
        v = np.ravel(v) if v.ndim > 1 else v
        s, p = kurtosistest(v, nan_policy=policy, alternative=alter)
        res.update({f'Kurtosis_({k})_statistic': s, f'Kurtosis_({k})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]])
@FuncTools.attach_attr(docstring=doc.hypoi_jb, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_jb(**params):
    from scipy.stats import jarque_bera
    res = {}
    for k, v in params.get('data').items():
        s, p = jarque_bera(v, axis=None)
        res.update({f'Jarque_Bera_({k})_statistic': s, f'Jarque_Bera_({k})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], f_exp=T[None: Optional[Iterable[int]]], ddf=T[0: int],
                          pd_lambda=T[1: Numeric])
@FuncTools.attach_attr(docstring=doc.hypoi_pd, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_pd(**params):
    from scipy.stats import power_divergence
    data, res, exp, ddf, pd_lam = (params.get('data'), {}, params.get('f_exp'), params.get('ddf'),
                                   params.get('pd_lambda'))
    for k, v in data.items():
        v = _ravel_all(v)[0]
        s, p = power_divergence(v, f_exp=exp, ddof=ddf, axis=0, lambda_=pd_lam)
        res.update({f'Power_Divergence_{k}_statistic': s, f'Power_Divergence_{k}_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], f_exp=T[None: Optional[Iterable[int]]], ddf=T[0: int])
@FuncTools.attach_attr(docstring=doc.hypoi_chi2, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoi_chi2(**params):
    from scipy.stats import chisquare
    data, res, exp, ddf = params.get('data'), {}, params.get('f_exp'), params.get('ddf')
    for k, v in data.items():
        v = _ravel_all(v)[0]
        s, p = chisquare(v, f_exp=exp, ddof=ddf, axis=0)
        res.update({f'Chi_Square_{k}_statistic': s, f'Chi_Square_{k}_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoj_pearson, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoj_pearson(**params):
    from scipy.stats import pearsonr
    data, alter, res = params.get('data'), params.get('alternative'), {}
    assert_info_raiser(_is_all_vals_related(data), ValueError('all input values should be of identical size'))
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = pearsonr(v1, v2, alternative=alter) if _has_no_nan(v1, v2) else (np.nan, np.nan)
        res.update({f'Pearson_({k1})*({k2})_statistic': s, f'Pearson_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoj_spearman, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoj_spearman(**params):
    from scipy.stats import spearmanr
    data, alter, policy, res = params.get('data'), params.get('alternative'), params.get('nan_policy'), {}
    assert_info_raiser(_is_all_vals_related(data), ValueError('all input values should be of identical size'))
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        s, p = spearmanr(v1, v2, axis=0, nan_policy=policy, alternative=alter)
        res.update({f'Spearman_({k1})*({k2})_statistic': s, f'Spearman_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']],
                          method=T['auto': Literal['auto', 'asymptotic', 'exact']],
                          kendall_tau=T['b': Literal['b', 'c', 'w']],
                          rank=T[True: bool], weigher=T[None: Optional[Callable]], additive=T[True: bool])
@FuncTools.attach_attr(docstring=doc.hypoj_kendall, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoj_kendall(**params):
    from scipy.stats import kendalltau, weightedtau
    data, res, policy, m, alter, tau = (params.get('data'), {}, params.get('nan_policy'), params.get('method'),
                                        params.get('alternative'), params.get('kendall_tau'))
    rank, weigher, additive = ((params.get('rank'), params.get('weigher'), params.get('additive'))
                               if tau == 'w' else [None for _ in range(3)])
    assert_info_raiser(_is_all_vals_related(data), ValueError('all input values should be of identical size'))
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        if tau in ['b', 'c']:
            s, p = kendalltau(v1, v2, nan_policy=policy, method=m, alternative=alter, variant=tau)
        else:  # weighted tau
            s, p = weightedtau(v1, v2, rank=rank, weigher=weigher, additive=additive)
        res.update({f'Kendall_{tau}_({k1})*({k2})_statistic': s, f'Kendall_{tau}_({k1})*({k2})_pvalue': p})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          nan_policy=T['propagate': Literal['omit', 'raise', 'propagate']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypoj_t, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, object]]])
def hypoj_t(**params):
    from scipy.stats import ttest_rel
    policy, alter, data, res = params.get('nan_policy'), params.get('alternative'), params.get('data'), {}
    assert_info_raiser(_is_all_vals_related(data), ValueError('all input values should be of identical size'))
    extra = params.get('~full_return', False)
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        _ = ttest_rel(v1, v2, nan_policy=policy, alternative=alter)
        res.update({f'T_related_({k1})*({k2})_statistic': _[0], f'T_related_({k1})*({k2})_pvalue': _[1]})
        if extra:
            ex = _dict_extra(_, ['df'])
            res.update({f'T_related_({k1})*({k2})_extra': ex})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], correction=T[False: bool],
                          zero_method=T['wilcox': Literal['wilcox', 'pratt', 'zsplit']],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']],
                          method=T['auto': Literal['auto', 'exact', 'approx']])
@FuncTools.attach_attr(docstring=doc.hypoj_rank, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, Numeric]]])
def hypoj_rank(**params):
    from scipy.stats import wilcoxon
    data, res = params.get('data'), {}
    m0, correction, alter, m = (params.get('zero_method'), params.get('correction'), params.get('alternative'),
                                params.get('method'))
    assert_info_raiser(_is_all_vals_related(data), ValueError('all input values should be of identical size'))
    extra = params.get('~full_return', False)
    for k1, k2 in combinations(list(data.keys()), 2):
        v1, v2 = _ravel_all(*(data.get(k1), data.get(k2)))
        _ = wilcoxon(v1, v2, zero_method=m0, correction=correction, alternative=alter, method=m)
        res.update({f'Wilcoxon_signed_rank_({k1})*({k2})_statistic': _[0],
                    f'Wilcoxon_signed_rank_({k1})*({k2})_pvalue': _[1]})
        if extra:
            ex = _dict_extra(_, ['zstatistic'])
            res.update({f'Wilcoxon_signed_rank_({k1})*({k2})_extra': ex})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]])
@FuncTools.attach_attr(docstring=doc.hypoj_friedman, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Numeric])
def hypoj_friedman(**params):
    from scipy.stats import friedmanchisquare
    data = params.get('data')
    assert_info_raiser(_is_all_vals_related(data), ValueError('all input values should be of identical size'))
    s, p = friedmanchisquare(*_ravel_all(*tuple(data.get(k) for k in data.keys())))
    return {'Friedman_statistic': s, 'Friedman_pvalue': p}


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]],
                          distance_criteria=T[lambda x, y: np.linalg.norm(x-y, ord=2, axis=0):
                                              Callable[[ndarray, ndarray], Numeric]],
                          n_resamples=T[1000: int], random_state=T[None: Optional[int]])
@FuncTools.attach_attr(docstring=doc.hypoj_mgc, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, Union[ndarray, list[int]]]]])
def hypoj_mgc(**params):
    from scipy.stats import multiscale_graphcorr
    data, res = params.get('data'), {}
    _dis, _reps, random_state = params.get('distance_criteria'), params.get('n_resamples'), params.get('random_state')
    assert_info_raiser(_is_all_mats_related(data),
                       ValueError('all input values should be matrix with identical size of rows'))
    dis = partial(distance_matrix, method=_dis)
    extra = params.get('~full_return', False)
    for k1, k2 in combinations(list(data.keys()), 2):
        m1, m2 = dis(data.get(k1)), dis(data.get(k2))
        s, p, _ = multiscale_graphcorr(m1, m2, compute_distance=None, reps=_reps, workers=1, is_twosamp=False,
                                       random_state=random_state) \
            if _has_no_nan(*_ravel_all(m1, m2)) else (np.nan, np.nan, None)
        res.update({f'Multiscale_Graph_Correlation_({k1})*({k2})_statistic': s,
                    f'Multiscale_Graph_Correlation_({k1})*({k2})_pvalue': p})
        if extra:
            res.update({f'Multiscale_Graph_Correlation_({k1})*({k2})_extra': _})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], dist=T[norm(loc=0, scale=1): dist],
                          n_resamples=T[9999: int], batch=T[None: Optional[int]],
                          agg_statistics=T[{'mean': lambda x: np.mean(x)}: dict[str, Callable[[ndarray], Numeric]]],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']])
@FuncTools.attach_attr(docstring=doc.hypos_mc, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, ndarray]]], **{'~unknown_tp': [dist]})
def hypos_mc(**params):
    from scipy.stats import monte_carlo_test
    data, res, _dis, _reps = params.get('data'), {}, params.get('dist'), params.get('n_resamples')
    fs, batch, alter = params.get('agg_statistics'), params.get('batch'), params.get('alternative')
    extra = params.get('~full_return', False)
    dis_set = [_dis] if not hasattr(_dis, '__len__') else _dis
    for dis in dis_set:
        name = dis.dist.name
        for k, v in data.items():
            v = _ravel_all(v)[0]
            for n, f in fs.items():
                _ = monte_carlo_test(v, dis.rvs, f, vectorized=False, n_resamples=_reps, batch=batch,
                                     alternative=alter, axis=0)
                s, p = (_.statistic, _.pvalue) if hasattr(_, 'statistic') and hasattr(_, 'pvalue') else (np.nan, np.nan)
                res.update({f'Monte_Carlo_({name}):({n})@({k})_statistic': s,
                            f'Monte_Carlo_({name}):({n})@({k})_pvalue': p})
                if extra:
                    ex = _dict_extra(_, ['null_distribution'])
                    res.update({f'Monte_Carlo_({name}):({n})@({k})_extra': ex})
    return res


@FuncTools.params_setting(data=T[Null: dict[str, ndarray]], n_resamples=T[9999: int],
                          permu_type=T['independent': Literal['independent', 'samples', 'pairings']],
                          binding_groups=T[2: lambda x: isinstance(x, int) and x >= 2], batch=T[None: Optional[int]],
                          agg_statistics=T[{'std_of_mean': lambda *x: np.std([np.mean(_) for _ in x])}:
                                           dict[str, Callable[[ndarray], Numeric]]],
                          alternative=T['two-sided': Literal['two-sided', 'less', 'greater']],
                          random_state=T[None: Optional[int]])
@FuncTools.attach_attr(docstring=doc.hypos_mc, info_func=True, entry_tp=dict[str, ndarray],
                       return_tp=dict[str, Union[Numeric, dict[str, ndarray]]], **{'~unknown_tp': [dist]})
def hypos_permu(**params):
    from scipy.stats import permutation_test
    data, res, p_type, _reps, grp = (params.get('data'), {}, params.get('permu_type'), params.get('n_resamples'),
                                     params.get('binding_groups'))
    assert_info_raiser(grp <= len(data), ValueError('binding_groups must no greater than data groups'))
    fs, batch, alter, seed = (params.get('agg_statistics'), params.get('batch'), params.get('alternative'),
                              params.get('random_state'))
    extra = params.get('~full_return', False)
    if p_type in ['samples', 'pairings']:
        assert_info_raiser(_is_all_vals_related(data), ValueError('all input values should be of identical size'))

    for k_set in combinations(list(data.keys()), grp):
        v_set = _ravel_all(*tuple(data.get(_) for _ in k_set))
        for n, f in fs.items():
            _ = permutation_test(v_set, f, permutation_type=p_type, vectorized=False, n_resamples=_reps,
                                 batch=batch, alternative=alter, axis=0, random_state=seed)
            s, p = (_.statistic, _.pvalue) if hasattr(_, 'statistic') and hasattr(_, 'pvalue') else (np.nan, np.nan)
            res.update({f"Permutation_({n})@({'*'.join(k_set)})_statistic": s,
                        f"Permutation_({n})@({'*'.join(k_set)})_pvalue": p})
            if extra:
                ex = _dict_extra(_, ['null_distribution'])
                res.update({f"Permutation_({n})@({'*'.join(k_set)})_extra": ex})
    return res


__all__ = [str(_) for _ in dir() if 'hypo' in _]


if __name__ == '__main__':
    pass
