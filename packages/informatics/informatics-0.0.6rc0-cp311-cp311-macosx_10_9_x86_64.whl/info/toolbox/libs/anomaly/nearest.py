from info.basic.functions import FuncTools, T, Null, default_param, assert_info_raiser
from info.basic.typehint import Numeric
from info import docfunc as doc
from typing import Optional, Literal, Callable
from numpy import ndarray
import numpy as np
from scipy.linalg import eig, ldl
from dataclasses import dataclass
from itertools import combinations
fun = __import__('info.basic.functions', fromlist=['_matrix_like'])
_matrix_duck = getattr(fun, '_matrix_like')
_vector_duck = getattr(fun, '_vector_like')
_init_lb = getattr(fun, '_init_prob')
_complex_lookup_table = getattr(fun, '_complex_lookup_table')
_rearrange_ka_map = getattr(fun, '_rearrange_ka_map')
_inverse_if_possible = getattr(fun, '_inverse_if_possible')
_get_f_statistic = getattr(fun, '_get_f_statistic')
_get_x_scale = getattr(fun, '_get_x_scale')
_merge_nearest_anomalies = getattr(fun, '_merge_nearest_anomalies')
__c_ij = getattr(fun, '__c_ij')


_convergence = (lambda x: np.sum(x / (x[0] + 1e-10)))  # agg function
_stop_iter_cond = (lambda _iter, _it_num=3, tol=0.1: np.std(_iter[-_it_num:]) < tol)


def _ka_opt(mp: ndarray, a: ndarray, k: ndarray, __vis: bool = False) -> tuple[int, float]:

    if __vis:
        # visualization for testing:
        # plt = __import__('matplotlib', fromlist=['pyplot']).pyplot
        # plt.imshow(mp, extent=(0, 200, 0, 300))
        # plt.show()
        from info.vis import visualization as vis
        vis.Canvas.play(data=mp, fig_type='image')
        vis.Canvas.play(data=mp.mean(axis=1))
        vis.Canvas.play(data=mp.mean(axis=0))

    opt_a = float(a[np.argmax(mp.mean(axis=1))])
    _ = np.diff(mp.mean(axis=0), n=1)  # idx +1 here
    _fast_decline_idx = np.argmin(_)
    opt_k = max(int(k[_fast_decline_idx] + 1), 4)  # k in [4, intrinsic_max_k]
    return opt_k, opt_a


@dataclass
class _KAMap:
    a_axis: ndarray = None
    k_axis: ndarray = None
    f_statistic: ndarray = None
    opt: tuple[int, float] = None

    def __init__(self, mp: ndarray, a_axis: ndarray, k_axis: ndarray, __ka_optimizer: Callable):
        self.f_statistic, self.thre_axis, self.k_axis = mp, a_axis, k_axis
        self.opt = __ka_optimizer(self.f_statistic, self.thre_axis, self.k_axis)


def _nearest_anomalies(idx: ndarray, ref: ndarray, frac: dict[int, float], k: int):
    _sf, *others = idx[:k+1]
    _y_self, ys = ref[_sf], ref[others]
    _count = {_: len(np.argwhere(ys == _)) for _ in np.unique(ref)}
    return _inverse_if_possible({p: [np.log10(_count[p[1]] + 1e-10) - np.log10(_count[p[0]] + 1e-10) -
                                    np.log10(frac[p[1]]) + np.log10(frac[p[0]]), _sf] for p in
                                 combinations(set(_count.keys()), 2)})


def _update_riemannian(trans: _matrix_duck, mu: list[float], k: int, _x: _matrix_duck, _y: _vector_duck,
                       eta: float, __dis_define: int) -> tuple[_matrix_duck, _vector_duck]:
    uni_labels = np.unique(_y)
    trans_x, idx = (trans @ _x.T).T, {_: np.where(_y == _)[0] for _ in uni_labels}
    _idx_ref = {s1: s2 for s1, s2 in zip(mu, idx.keys())}  # prob -> uni
    _inv_idx_ref = {s2: s1 for s1, s2 in _idx_ref.items()}  # uni -> prob

    minus = ((_x.T @ _merge_cmat(trans_x, _y, k, uni_labels, idx, _idx_ref, _inv_idx_ref, __dis_define) @ _x) *
             (eta / _x.shape[0]))
    _new_a = (trans.T @ trans).real - minus

    res = eig(_new_a, b=None, left=None, right=True, homogeneous_eigvals=False)
    _new_c = np.array([_ if _ >= 0 else 0 for _ in res[0].real])
    res = res[1] @ np.diag(_new_c) @ res[1].T
    lu, _d, _perm = ldl(res)
    return np.sqrt(_d.astype(complex)) @ lu.T, _new_c


def _merge_cmat(trans_x, y, k, uni_labels, idx, _idx_ref, _inv_idx_ref, __dis):
    res = np.zeros((trans_x.shape[0], trans_x.shape[0]))
    # trees = {_: KDTree(trans_x[idx.get(_)]) for _ in uni_labels}  # KDTree do not support complex, await scipy team
    trees = {_: trans_x[idx.get(_)] for _ in uni_labels}
    for tx, _lb in zip(trans_x, y):
        # _distance, _idx = trees.get(_lb).query(tx, k+1)  # KDtree uses Euclidean as default
        _distance, _idx = _complex_lookup_table(trees.get(_lb), tx, k, __dis)
        ref_dis = _distance[1:]**2 + 1
        _md = {_inv_idx_ref.get(_): np.linalg.norm(trans_x[idx.get(_)], axis=1, ord=__dis) for _ in uni_labels
               if _ != _lb}
        _j_idx, _idx_now = {_inv_idx_ref.get(_lb): _idx[1:]}, _idx[0]
        _l_ids = {k: {_m: idx.get(_idx_ref.get(k))[np.where((_dis - v) >= 0)] for _dis, _m in
                      zip(ref_dis, _j_idx.get(_inv_idx_ref.get(_lb)))} for k, v in _md.items()}
        res += _c_maker(trans_x.shape[0], int(_idx_now), _j_idx, _l_ids)
    return res


def _c_maker(dims: int, id_now: int, j_set: dict[float, ndarray],
             l_set: dict[float, dict[int, ndarray]]) -> ndarray:
    res = np.zeros((dims, dims))

    for mu_l, v in l_set.items():

        for id_j, _v in v.items():
            res += __c_ij(res, id_now, id_j, list(j_set.keys())[0])
            res += np.sum([__c_ij(res, id_now, id_j, 1) - __c_ij(res, id_now, id_l, 1)
                           for id_l in _v], axis=0) * mu_l  # 0.0 if empty
    return res


class Neighbors:

    @FuncTools.params_setting(data=T[Null: object], labels=T[Null: ndarray], distance_measure=T[2: int],
                              kamap_optimizer=T[_ka_opt: Callable[[ndarray, ndarray, ndarray], tuple[int, float]]],
                              nearing_mode=T['LMNN': Literal['KNN', 'LMNN']],
                              k_determine=T[10: int], eta_determine=T[0.05: float],
                              prior_prob_determine=T[None: Optional[list[float]]],
                              **{'~converge_statistic': T[_convergence: Callable[[ndarray], Numeric]],
                                 '~stop_iter_cond': T[_stop_iter_cond: Callable[[list[Numeric]], bool]],
                                 '~max_k_determine': T[None: Optional[int]],
                                 '~verbosity': T[True: bool]})
    def __init__(self, **params):
        self.settings = {k: v for k, v in params.items() if k in ['distance_measure', 'kamap_optimizer',
                                                                  'nearing_mode', 'k_determine', 'eta_determine',
                                                                  'prior_prob_determine', '~converge_statistic',
                                                                  '~stop_iter_cond', '~max_k_determine', '~verbosity']}
        self.x, self.y, self.trans, self.thre = [None for _ in range(4)]
        self.update(**params)

    def update(self, **params):
        md, dt, lb = self.settings.get('nearing_mode'), params.get('data'), params.get('labels')

        if md == 'KNN':
            self.trans = np.eye(dt.shape[1])
        elif md == 'LMNN':
            k, eta = self.settings.get('k_determine'), self.settings.get('eta_determine')
            mu = default_param(self.settings, 'prior_prob_determine', _init_lb(lb))
            assert_info_raiser(np.sum(mu) == 1.0, ValueError('prior probability should sum into 1.'))
            _conv_static, _stop_cond, _vb = (self.settings.get('~converge_statistic'),
                                             self.settings.get('~stop_iter_cond'), self.settings.get('~verbosity'))
            self.trans = self._converge_trans(np.eye(dt.shape[1]), mu, k, dt, lb, eta, _conv_static, _stop_cond,
                                              self.settings.get('distance_measure'), _vb)
        else:  # await for extensions, never entry
            raise NotImplementedError(f'mode {md} is not implemented yet.')

        self.x = np.vstack([self.x, dt]) if self.x is not None else dt
        self.y = np.concatenate([self.y, lb], axis=0) if self.y is not None else lb
        self._cal_dissimilarities(opt='optimize')

    @staticmethod
    def _converge_trans(trans: _matrix_duck, mu: list[float], k: int, _x: _matrix_duck, _y: _vector_duck,
                        eta: float, __conv_static: Callable, __stop_cond: Callable, __dis_define: int,
                        __prompt: bool) -> _matrix_duck:
        # trans will be like: _x @ (trans.T @ trans) @ _x.T => spatial trans is: (trans @ _x.T).T
        _ = print(' pre-processing starts '.join(['-'*30 for _ in range(2)])) if __prompt else ...
        _static = [-600, -900, -300]  # use for init
        count = 1
        while not __stop_cond(_static):
            trans, _ref = _update_riemannian(trans, mu, k, _x, _y, eta, __dis_define)
            _value = __conv_static(_ref)
            _static.append(_value)
            if __prompt:
                print(f'pre-training step {count}: current statistic is {_value}, waiting convergence of '
                      f'Riemannian metric...')
            count += 1
        return trans

    def _cal_dissimilarities(self, opt: Literal['optimize', 'update'], _x: _matrix_duck = None,
                             _ka: _KAMap = None):
        pi = np.unique(self.y, return_counts=True)
        _pi_sum, _dis = sum(pi[1]), self.settings.get('distance_measure')
        frac = {_m1: _m2 / _pi_sum for _m1, _m2 in zip(pi[0], pi[1])}
        _comp_vecs = (self.trans @ self.x.T).T
        if opt == 'optimize':
            _optimizer = self.settings.get('kamap_optimizer')
            lut = np.array([np.argsort(np.linalg.norm(_comp_vecs - _, ord=_dis, axis=1)) for _ in _comp_vecs])
            k_range = (_k if (_k := self.settings.get('~max_k_determine')) is not None else
                       self.settings.get('k_determine'))
            a_lut = {k: _merge_nearest_anomalies([_nearest_anomalies(_ref, self.y, frac, k) for _ref in lut]) for
                     k in [int(_ + 1) for _ in range(k_range - 1)]}  # -1 for 1st self; ~max_k_determine for fig export
            _a_k_maps, a_axis = _get_f_statistic(a_lut, self.y, _get_x_scale(a_lut))
            ak_maps, k_axis = _rearrange_ka_map(_a_k_maps)
            self.thre = {k: _KAMap(v, a_axis.get(k), k_axis, _optimizer) for k, v in
                         ak_maps.items()}
        else:  # update
            _data_vecs = (self.trans @ _x.T).T
            lut = {k: np.array([np.argsort(np.linalg.norm(_comp_vecs - _, ord=_dis, axis=1))[:v.opt[0]]
                                for _ in _data_vecs]) for k, v in self.thre.items()}
            return {k: _merge_nearest_anomalies([_nearest_anomalies(_ref, self.y, frac, self.thre.get(k).opt[0])
                                                 for _ref in v], True).get(k) for k, v in lut.items()}

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def predict_dissimilarity(self, **params):
        return self._cal_dissimilarities('update', params.get('data'), self.thre)

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def predict(self, **params):
        _dt = params.get('data')
        _dis, _k_vec = self.predict_dissimilarity(**params), set()
        _ = [_k_vec := _k_vec.union(k) for k in _dis.keys()]
        mu = default_param(self.settings, 'prior_prob_determine', _init_lb(self.y))
        _med = {k: v - self.thre.get(k).opt[1] for k, v in _dis.items()}
        _res = {k: np.zeros(_dt.shape[0]) for k in _k_vec}
        for k, v in _med.items():
            ptr1 = _res.get(k[0])
            ptr1 += v * mu[k[0]]
            ptr2 = _res.get(k[1])
            ptr2 -= v * mu[k[1]]
        return np.argmin(np.array([v for k, v in _res.items()]).T, axis=1)


doc.redoc(Neighbors, doc.Neighbors)


if __name__ == '__main__':
    pass
