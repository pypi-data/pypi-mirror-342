from info.basic.decorators import FuncTools
from info.basic.functions import assert_info_raiser
from info.basic.typehint import DirTP, T, Null
from info import docfunc as doc
from typing import Union, Optional
from scipy.stats import dirichlet
from scipy.stats import multinomial as st_multinomial
from scipy.sparse import spmatrix, sparray
import scipy.sparse as sp
from numpy import ndarray
import numpy as np
_bayes_hook = __import__('info.toolbox.libs.bayes._frame', fromlist=['_Bayes'])
fun = __import__('info.basic.functions', fromlist=['nbayes_anomaly'])
Bayes = getattr(_bayes_hook, 'Bayes')
multinomial = getattr(_bayes_hook, 'multinomial')
SparseArray = Union[sparray, spmatrix]
GenericArray = Union[ndarray, SparseArray]
_harmonic_mean = getattr(fun, '_harmonic_mean')
_matrix_duck = getattr(fun, '_matrix_like')
a = getattr(fun, 'nbayes_anomaly')


def _k_folder(obj: Union[ndarray, SparseArray], rate: float) -> tuple[Union[ndarray, SparseArray]]:
    _idx = np.arange(obj.shape[0])
    split_idx = np.array_split(_idx, int(1/rate))

    def complementary_idx(s: Union[ndarray, SparseArray], x: Union[ndarray, SparseArray]) -> ndarray:
        return np.array(list(set(s).difference(set(x))))

    for _ in range(len(split_idx)):
        yield obj[complementary_idx(_idx, split_idx[_])], obj[split_idx[_]]  # train, test


def _cv_splitter(x: ndarray, rate: float) -> tuple[ndarray]:
    uni = np.unique(x)
    _mediate = [np.where(x == item)[0] for item in uni]
    gen = [_k_folder(_mediate[_], rate) for _ in range(len(_mediate))]  # stratified
    s = [[(train, test) for train, test in gen[_]] for _ in range(len(gen))]
    for j in range(len(s[0])):
        tr, ts = [], []
        for i in range(len(s)):
            tr.append(s[i][j][0])
            ts.append(s[i][j][1])
        yield tr, ts


def _v_stack(x1: GenericArray, x2: GenericArray) -> GenericArray:
    return np.vstack([x1, x2]) if (isinstance(x1, ndarray) and isinstance(x2, ndarray)) else sp.vstack([x1, x2])


def _classes_idx(x: ndarray) -> tuple[ndarray, ...]:
    uni = np.unique(x)
    return tuple(np.where(x == item)[0] for item in uni)


def _cv_score(_idx, x, model):
    tr = [x[_idx[0][0]], x[_idx[0][1]]]
    ts = [x[_idx[1][0]], x[_idx[1][1]]]
    tr_lb = np.concatenate([np.repeat(0, tr[0].shape[0]), np.repeat(1, tr[1].shape[0])], axis=0)
    ts_lb = np.concatenate([np.repeat(0, ts[0].shape[0]), np.repeat(1, ts[1].shape[0])], axis=0)
    tr_a, _ = _a_updater(_v_stack(tr[0], tr[1]), tr_lb, [_.conjugate for _ in model], model, False)
    ts_stack = _v_stack(ts[0], ts[1])
    ts_stack = getattr(ts_stack, 'toarray')() if not isinstance(ts_stack, ndarray) else ts_stack
    err_array = np.array([np.dot(_, tr_a) for _ in ts_stack])
    return _harmonic_mean([err_array, ts_lb])


def _a_updater(x: GenericArray, idx: ndarray, prior: list[DirTP], _bayes: list[Bayes],
               use_update: bool = True) -> tuple[ndarray, list[Bayes]]:
    idx = _classes_idx(idx)
    probs = [getattr(_, 'toarray')() if not isinstance(_, ndarray) else _ for _ in [x[_idx] for _idx in idx]]  # dense
    probs = [_.sum(axis=0) for _ in probs]  # list[vector]
    conj = [st_multinomial(v1.sum(), (v1 / v1.sum())) for v1 in probs]
    if _bayes is None:  # conj -> kernel;
        models = [multinomial(kernel=v1, prior=v2) for v1, v2 in zip(conj, prior)]
        dissimilarities = np.log(models[0].conjugate.alpha) - np.log(models[1].conjugate.alpha)
    else:  # conj -> posterior;
        if use_update:
            _ = [v2.update_posterior(posterior=v1) for v1, v2 in zip(conj, _bayes)]
            models = _bayes  # pointer reset
            dissimilarities = np.log(models[0].conjugate.alpha) - np.log(models[1].conjugate.alpha)
        else:
            models = _bayes
            _dis = [v2.compare_posterior(posterior=v1).alpha for v1, v2 in zip(conj, models)]
            dissimilarities = np.log(_dis[0]) - np.log(_dis[1])
    return dissimilarities, models  # dissimilarities, model


_is_label_array = (lambda x: hasattr(x, 'ndim') and x.ndim == 1 and x.dtype == bool)  # [0, 1], 1 for anomaly
_unknown_tp = list(getattr(SparseArray, '__args__')) + [DirTP]


class NaiveBayes:

    @FuncTools.params_setting(data=T[Null: _matrix_duck], priori=T[None: Optional[list[DirTP]]],
                              validation_rate=T[0.2: float], model_lightweight=T[True: bool],
                              **{'~unknown_tp': _unknown_tp})
    def __init__(self, **params):
        self.settings = {k: v for k, v in params.items() if k in ['validation_rate', 'model_lightweight']}
        self.X, self.y, self.a, self.bayes_model, self.threshold = [None for _ in range(5)]
        self.update(**params)

    @FuncTools.params_setting(data=T[Null: _matrix_duck], labels=T[Null: lambda x: _is_label_array(x)],
                              prior=T[None: Optional[list[DirTP]]], **{'~unknown_tp': _unknown_tp})
    def update(self, **params):
        _x, _y = params.get('data'), params.get('labels')
        assert_info_raiser(_x.shape[0] == _y.shape[0], ValueError('update data and labels are of different size.'))
        _p = [dirichlet([1 for _ in range(int(_x.shape[1]))]) for _1 in
              range(2)] if not (_m := params.get('prior')) else _m
        _, self.bayes_model = _a_updater(_x, _y, _p, self.bayes_model)
        if not self.settings.get('model_lightweight'):   # otherwise no cache for data, pure statistical computing
            self.X = _x if self.X is None else _v_stack(self.X, _x)
            self.y = _y if self.y is None else np.concatenate([self.y, _y], axis=0)
            self.a = _ if self.a is None else np.concatenate([self.a, _], axis=0)
        idx = [[tr, ts] for tr, ts in _cv_splitter(_y, self.settings.get('validation_rate'))]
        self.threshold = np.array([_cv_score(item, _x, self.bayes_model)
                                   for item in idx]).max()  # conservative estimation to adapt sparse array

    @FuncTools.params_setting(data=T[Null: _matrix_duck], **{'~unknown_tp': _unknown_tp})
    def predict_dissimilarity(self, **params):
        return a(params.get('data'), self.bayes_model)

    @FuncTools.params_setting(data=T[Null: _matrix_duck], **{'~unknown_tp': _unknown_tp})
    def predict(self, **params):
        return self.predict_dissimilarity(data=params.get('data')) <= self.threshold


doc.redoc(NaiveBayes, doc.NaiveBayes)


if __name__ == '__main__':
    pass
