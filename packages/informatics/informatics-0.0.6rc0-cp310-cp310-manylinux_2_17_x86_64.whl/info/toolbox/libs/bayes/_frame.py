from info.basic.decorators import FuncTools
from info.basic.typehint import (T, Null, BernBinTP, CatMultTP, BetaTP, DirTP, DirMultTP, PoiTP, GamTP, ExpTP, ErlTP,
                                 NbinTP, GauTP, MGauTP, WisTP, StuTP, GauWisTP)
from info.basic.core import GenericDiscrete
from info.basic.functions import assert_info_raiser
from info import docfunc as doc
from typing import Callable, TypeVar, Optional, Union
from functools import partial
from scipy import stats as st
from numpy import ndarray
import numpy as np
Dis = object
PriDis = TypeVar('PriDis')
PosDis = TypeVar('PosDis')
LikeDis = TypeVar('LikeDis')
LikeData = TypeVar('LikeData')
PreDis = TypeVar('PreDis')


class Bayes:

    @FuncTools.params_setting(name=T[Null: str], kernel=T[Null: Dis], prior=T[Null: Dis],
                              likelihood_check=T[Null: Callable[[PosDis], bool]],
                              update_conjugate=T[Null: Callable[[PriDis, Union[LikeDis, LikeData]], PosDis]],
                              update_predictive=T[Null: Callable[[PosDis, Union[LikeDis, LikeData]], PreDis]])
    def __init__(self, **params):
        self.name = params.get('name')
        self.kernel = params.get('kernel')
        self.conjugate = params.get('prior')
        self.predictive, self._err_pos = None, ValueError('use a mismatch posterior from kernel')
        self._valid_like = params.get('likelihood_check')
        self.update_conjugate = params.get('update_conjugate')
        self.update_predictive = params.get('update_predictive')
        self.update_posterior()

    @FuncTools.params_setting(posterior=T[None: Optional[Dis]])
    def update_posterior(self, **params):
        posterior = params.get('posterior')
        if posterior is None:
            self._update_posterior()
            self._update_predictive()
        else:  # update via ndarray data or distributions
            assert_info_raiser(self._valid_like(posterior), self._err_pos)
            self.conjugate = self.update_conjugate(self.conjugate, posterior)
            self.predictive = self.update_predictive(self.conjugate, posterior)

    @FuncTools.params_setting(posterior=T[Null: Dis])
    def compare_posterior(self, **params):
        posterior = params.get('posterior')
        assert_info_raiser(self._valid_posterior(posterior), self._err_pos)
        return self.update_conjugate(self.conjugate, posterior)

    def _update_posterior(self):
        self.conjugate = self.update_conjugate(self.conjugate, self.kernel)

    def _update_predictive(self):
        self.predictive = self.update_predictive(self.conjugate, self.kernel)

    def _valid_posterior(self, x: PosDis) -> bool:
        return type(self.conjugate) is type(x)


doc.redoc(Bayes, doc.Bayes)


def _as_multinomial(x: LikeDis):
    if hasattr(x, 'dist') and x.dist.name in ['bernoulli', 'binom']:
        if x.dist.name == 'bernoulli':
            p = x.kwds.get('p', x.args[0])
            res = st.multinomial(1, [1-p, p])
        else:
            n, p = x.kwds.get('n', x.args[0]), x.kwds.get('p', x.args[1])
            res = st.multinomial(n, p)
    else:  # categorical or multinomial
        res = x
    return res


def _multinomial_conjugate(pri: DirTP, like: Union[LikeDis, LikeData]) -> DirTP:  # dirichlet * like -> dirichlet
    if hasattr(like, 'dist') and like.dist.name in ['bernoulli', 'binom']:
        like = _as_multinomial(like)
    if not isinstance(like, ndarray):  # multinomial distribution
        n, p = like.n, like.p
        _vec = n * p
    else:
        _vec = like.sum(axis=0)
    return st.dirichlet(_vec + pri.alpha)


def _multinomial_predictive(pos: DirTP, like: Union[LikeDis, LikeData]) -> DirMultTP:
    # dirichlet * like -> dirichlet multinomial
    if hasattr(like, 'dist') and like.dist.name in ['bernoulli', 'binom']:
        like = _as_multinomial(like)
    if not isinstance(like, ndarray):  # multinomial distribution
        n = like.n
    else:
        n = np.unique(like.sum(axis=1))[0]
    return st.dirichlet_multinomial(pos.alpha, n)


def _discrete_pre_check(p: DirTP, k: GenericDiscrete) -> bool:
    if hasattr(k, 'name') and k.name in ['bernoulli', 'binomial']:
        res = k.p.__len__() == p.alpha.__len__() == 2
    else:
        res = k.p.__len__() == p.alpha.__len__()
    return res


def _init_prior(k: GenericDiscrete, p: Union[DirTP, BetaTP] = None) -> DirTP:
    res = st.dirichlet([1 for _ in range(len(k.p))]) if p is None else p
    return [x := res.args[0:2], st.dirichlet([_/sum(x) for _ in x])][-1] if (hasattr(res, 'dist') and
                                                                             res.dist.name == 'beta') else res


_observe_to_multi = (lambda x: GenericDiscrete(x) if not isinstance(x, GenericDiscrete) else x)  # generic discrete


def _check_discrete_likelihood(dis_name: str):

    def __inner(_x: Union[LikeDis, LikeData], _dis_name: str) -> bool:
        res = False
        if _dis_name == 'bernoulli':
            if hasattr(_x, 'dist') and _x.dist.name == 'bernoulli':  # init by st.bernoulli
                res = True
            elif hasattr(_x, 'n') and hasattr(_x, 'p'):  # init by st.multinomial
                res = True if (_x.n == 1 and len(_x.p) == 2) else False
            elif isinstance(_x, ndarray) and _x.ndim == 2:  # data: [[0, 1], [1, 0], [0, 1]] instead of [1, 0, 1]
                _temp = _x.sum(axis=1)
                res = all([_ == 1 for _ in _temp])
        elif _dis_name == 'binomial':
            if hasattr(_x, 'dist') and _x.dist.name == 'binom':  # init by st.binom
                res = True
            elif hasattr(_x, 'n') and hasattr(_x, 'p'):  # init by st.multinomial
                res = True if len(_x.p) == 2 else False
            elif isinstance(_x, ndarray) and _x.ndim == 2:  # data: [[0, 3], [1, 2], [2, 1]] instead of [3, 2, 1]
                _temp = _x.sum(axis=1)
                res = np.unique(_temp).__len__() == 1
        elif _dis_name == 'categorical':
            if hasattr(_x, 'n') and hasattr(_x, 'p'):  # init by st.multinomial
                res = True if (_x.n == 1 and len(_x.p) >= 2) else False
            elif isinstance(_x, ndarray) and _x.ndim == 2:  # data: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
                _temp = _x.sum(axis=1)
                res = np.unique(_temp).__len__() == 1 and np.unique(_temp)[0] == 1
        else:  # multinomial
            if hasattr(_x, 'n') and hasattr(_x, 'p'):  # init by st.multinomial
                res = True if (_x.n >= 1 and len(_x.p) >= 2) else False
            elif isinstance(_x, ndarray) and _x.ndim == 2:  # data: [[1, 0, 2], [1, 1, 1], [0, 2, 1]]
                _temp = _x.sum(axis=1)
                res = np.unique(_temp).__len__() == 1

        return res

    return partial(__inner, _dis_name=dis_name)


def _discrete_base(**params):
    kernel = _observe_to_multi(params.get('kernel'))
    prior = _init_prior(kernel, params.get('prior'))
    _check_like = params.get('likelihood_check')
    assert_info_raiser(kernel.name == params.get('~specific_distribution') and _discrete_pre_check(prior, kernel),
                       ValueError('mismatch of kernel and prior'))
    return Bayes(name=kernel.name, kernel=kernel, prior=prior, update_conjugate=_multinomial_conjugate,
                 update_predictive=_multinomial_predictive, likelihood_check=_check_like)


@FuncTools.params_setting(kernel=T[Null: BernBinTP], prior=T[None: Optional[Union[BetaTP, DirTP]]],
                          **{'~unknown_tp': [BernBinTP, BetaTP, DirTP]})
@FuncTools.attach_attr(docstring=doc.bernoulli)
def bernoulli(**params):
    return _discrete_base(**{**params, **{'~specific_distribution': 'bernoulli',
                                          'likelihood_check': _check_discrete_likelihood('bernoulli')}})


@FuncTools.params_setting(kernel=T[Null: CatMultTP], prior=T[None: Optional[DirTP]],
                          **{'~unknown_tp': [CatMultTP, DirTP]})
@FuncTools.attach_attr(docstring=doc.categorical)
def categorical(**params):  # no scipy api for categorical, init prior use scipy.stats.multinomial(1, p) instead
    return _discrete_base(**{**params, **{'~specific_distribution': 'categorical',
                                          'likelihood_check': _check_discrete_likelihood('categorical')}})


@FuncTools.params_setting(kernel=T[Null: BernBinTP], prior=T[None: Optional[Union[BetaTP, DirTP]]],
                          **{'~unknown_tp': [BernBinTP, BetaTP, DirTP]})
@FuncTools.attach_attr(docstring=doc.binomial)
def binomial(**params):
    return _discrete_base(**{**params, **{'~specific_distribution': 'binomial',
                                          'likelihood_check': _check_discrete_likelihood('binomial')}})


@FuncTools.params_setting(kernel=T[Null: CatMultTP], prior=T[None: Optional[DirTP]],
                          **{'~unknown_tp': [CatMultTP, DirTP]})
@FuncTools.attach_attr(docstring=doc.multinomial)
def multinomial(**params):
    return _discrete_base(**{**params, **{'~specific_distribution': 'multinomial',
                                          'likelihood_check': _check_discrete_likelihood('multinomial')}})


def _init_poisson_gam(x: PoiTP, pri: Union[GamTP, ExpTP, ErlTP] = None, __poi: bool = True):
    _args, _kwd = x.args, x.kwds
    mu, loc = _kwd.get('mu', _args[0]), _kwd.get('loc', _args[1] if len(_args) > 1 else 0)
    poi = st.poisson(mu-loc, 0)
    if pri is not None:
        _args, _kwd = pri.args, pri.kwds
        if pri.dist.name in ['gamma', 'erlang']:
            alpha, beta_inv = _kwd.get('a', _args[0]), _kwd.get('scale', _args[2] if len(_args) > 2 else 1)
        elif pri.dist.name == 'expon':
            alpha, beta_inv = 1, _kwd.get('scale', _args[0])
        else:
            alpha, beta_inv = 1, 1
        gam = st.gamma(alpha, 0, beta_inv)
    else:
        gam = st.gamma(poi.args[0], 0, 1)
    return poi if __poi else gam


def _poisson_conjugate(pri: GamTP, like: Union[LikeDis, LikeData]) -> GamTP:  # gamma * like -> gamma
    _args, _kwd = pri.args, pri.kwds
    alpha, beta_inv = _kwd.get('a', _args[0]), _kwd.get('scale', _args[2] if len(_args) > 2 else 1)
    if isinstance(like, ndarray):
        aug_a, aug_b = np.sum(like), len(like)
    else:  # instance of st.poisson
        aug_a, aug_b = like.kwds.get('mu', like.args[0]), 1  # treat poisson distribution as single test
    return st.gamma(alpha+aug_a, 0, 1/(aug_b + (1/beta_inv)))


def _poisson_predictive(pos: GamTP, like: Union[LikeDis, LikeData]) -> NbinTP:  # gamma * like -> negative binomial
    _args, _kwd, _ = pos.args, pos.kwds, like  # no use for like
    alpha, beta = _kwd.get('a', _args[0]), 1/_kwd.get('scale', _args[2] if len(_args) > 2 else 1)
    return st.nbinom(int(alpha), beta/(beta+1))


def _check_poisson(x: Union[LikeDis, LikeData]) -> bool:
    res = False
    if hasattr(x, 'dist') and x.dist.name == 'poisson':
        res = True
    elif isinstance(x, ndarray) and x.ndim == 1 and x.dtype == int:
        if np.all(x >= 0):
            res = True
    return res


@FuncTools.params_setting(kernel=T[Null: PoiTP], prior=T[None: Optional[GamTP]], **{'~unknown_tp': [PoiTP, GamTP]})
@FuncTools.attach_attr(docstring=doc.poisson)
def poisson(**params):
    kernel = _init_poisson_gam(params.get('kernel'))
    prior = _init_poisson_gam(kernel, params.get('prior'), False)
    return Bayes(name='poisson', kernel=kernel, prior=prior, update_conjugate=_poisson_conjugate,
                 update_predictive=_poisson_predictive, likelihood_check=_check_poisson)


GaussianWishart = type('GaussianWishart', (GauWisTP, ),
                       {'__new__': lambda cls, *m: [_temp := GauWisTP(*m),
                                                    _temp if getattr(_temp, '_is_valid')() else
                                                    GauWisTP(m[0], m[1], m[2], np.eye(len(m[0])))][-1]})


doc.redoc(GaussianWishart, doc.GaussianWishart)


def _init_gauss(x: Union[GauTP, MGauTP]) -> MGauTP:
    return st.multivariate_normal(np.asarray(x.mean())[..., np.newaxis],
                                  np.asarray(x.var())[..., np.newaxis, np.newaxis]) if (hasattr(x, 'dist') and
                                                                                        x.dist.name == 'norm') else x


def _infer_gaussian_prior(x: MGauTP, p: Union[GauTP, GamTP, MGauTP, WisTP, GauWisTP]) -> Union[MGauTP, WisTP, GauWisTP]:
    _dim, _pri = x.dim, p
    if p == 0:  # invalid GauWisTP
        from warnings import warn
        warn('invalid Gaussian-Wishart distribution, use default initial methods')
    res = GaussianWishart(np.array([0 for _ in range(_dim)]), 1, _dim,
                          np.eye(_dim)) if _pri in [None, 0] else _pri
    if hasattr(res, 'dist') and res.dist.name == 'gamma':
        _args, _kwd = res.args, res.kwds
        nu, w = 2 * _kwd.get('a', _args[0]), _kwd.get('scale', _args[2] if len(_args) > 2 else 1) / 2
        res = st.wishart(nu, w)
    elif hasattr(res, 'dist') and res.dist.name == 'norm':
        _args, _kwd = res.args, res.kwds
        m, sigma = _kwd.get('loc', _args[0]), _kwd.get('scale', _args[1] if len(_args) > 1 else 1)
        res = st.multivariate_normal(m, sigma)
    return res


def _check_gauss(x: Union[LikeDis, LikeData]) -> bool:
    res = False
    if isinstance(x, ndarray):
        if x.ndim == 2:
            res = True
    else:  # GauTP, MGauTP
        if hasattr(x, 'dist') and x.dist.name == 'norm':
            res = True
        elif hasattr(x, 'mean') and hasattr(x, 'cov'):
            res = True
    return res


def _gauss_conj_mu_sigma(pri: GauWisTP, like: Union[LikeDis, LikeData]) -> GauWisTP:
    if isinstance(like, ndarray):  # design mat
        _beta, _nu = pri.beta + like.shape[0], pri.nu + like.shape[0]
        _mean = (1/_beta) * (like.sum(axis=0) + pri.beta * pri.mean)
        _w_inv = (like.T @ like + pri.beta * (pri.mean[..., np.newaxis] @ pri.mean[..., np.newaxis].T) -
                  _beta * (_mean[..., np.newaxis] @ _mean[..., np.newaxis].T) + np.linalg.pinv(pri.w))
    else:  # treat MGauTP multivariate gaussian as single test
        like = _init_gauss(like)  # GauTP -> MGauTP
        _beta, _nu, _xn = pri.beta + 1, pri.nu + 1, like.mean
        _mean = (1 / _beta) * (_xn + pri.beta * pri.mean)
        _w_inv = (_xn[..., np.newaxis] @ _xn[..., np.newaxis].T +
                  pri.beta * (pri.mean[..., np.newaxis] @ pri.mean[..., np.newaxis].T) -
                  _beta * (_mean[..., np.newaxis] @ _mean[..., np.newaxis].T) + np.linalg.pinv(pri.w))
    return GaussianWishart(_mean, _beta, _nu, np.linalg.pinv(_w_inv))


def _gauss_pred_mu_sigma(pos: GauWisTP, like: Union[LikeDis, LikeData]) -> StuTP:
    mean, nu, _ = pos.mean, 1 + pos.nu - len(pos.mean), like
    _lambda = ((nu * pos.beta) / (1 + pos.beta)) * pos.w
    return st.multivariate_t(mean, np.linalg.pinv(_lambda), nu)


def _gauss_conj_mu(pri: MGauTP, like: Union[LikeDis, LikeData], precision: ndarray) -> MGauTP:
    _lambda = (like.shape[0] * precision + np.linalg.pinv(pri.cov) if isinstance(like, ndarray)
               else [pri := _init_gauss(pri), precision + np.linalg.pinv(pri.cov)][-1])  # treat MGauTP as single test
    _mean = (np.linalg.pinv(_lambda) @ (precision @ (like.sum(axis=0) if isinstance(like, ndarray)
             else [_p := _init_gauss(like), _p.mean][-1]) + np.linalg.pinv(pri.cov) @ pri.mean))
    return st.multivariate_normal(_mean, np.linalg.pinv(_lambda))


def _gauss_pred_mu(pos: MGauTP, like: Union[LikeDis, LikeData], precision: ndarray) -> MGauTP:
    _lambda_inv, _ = np.linalg.pinv(precision) + pos.cov, like
    _mean = pos.mean
    return st.multivariate_normal(_mean, _lambda_inv)


def _gauss_conj_sigma(pri: WisTP, like: Union[LikeDis, LikeData], mu: ndarray) -> WisTP:
    if isinstance(like, ndarray):  # design mat
        _design = like - mu
        _w, _nu = np.linalg.pinv(_design.T @ _design + np.linalg.pinv(pri.scale)), like.shape[0] + pri.df
    else:  # treat MGauTP as single test
        _w, _nu = np.linalg.pinv(np.linalg.pinv(like.cov) + np.linalg.pinv(pri.scale)), 1 + pri.df
    return st.wishart(_nu, _w)


def _gauss_pred_sigma(pos: WisTP, like: Union[LikeDis, LikeData], mu: ndarray) -> StuTP:
    mean, nu, _ = mu, 1 + pos.df - len(mu), like
    _lambda = nu * pos.scale
    return st.multivariate_t(mean, np.linalg.pinv(_lambda), nu)


@FuncTools.params_setting(kernel=T[Null: Union[GauTP, MGauTP]],
                          prior=T[None: Optional[Union[GauTP, GamTP, MGauTP, WisTP, GauWisTP]]],
                          **{'~unknown_tp': [GauTP, GamTP, MGauTP, WisTP, GauWisTP]})
@FuncTools.attach_attr(docstring=doc.gaussian)
def gaussian(**params):
    kernel = _init_gauss(params.get('kernel'))
    prior = _infer_gaussian_prior(kernel, params.get('prior'))  # can be initiated when None

    if isinstance(prior, MGauTP):
        res = Bayes(name='gaussian', kernel=kernel, prior=prior, likelihood_check=_check_gauss,
                    update_conjugate=partial(_gauss_conj_mu, precision=np.linalg.pinv(kernel.cov)),
                    update_predictive=partial(_gauss_pred_mu, precision=np.linalg.pinv(kernel.cov)))
    elif isinstance(prior, WisTP):
        res = Bayes(name='gaussian', kernel=kernel, prior=prior, likelihood_check=_check_gauss,
                    update_conjugate=partial(_gauss_conj_sigma, mu=kernel.mean),
                    update_predictive=partial(_gauss_pred_sigma, mu=kernel.mean))
    else:  # GauWisTP
        res = Bayes(name='gaussian', kernel=kernel, prior=prior, update_conjugate=_gauss_conj_mu_sigma,
                    update_predictive=_gauss_pred_mu_sigma, likelihood_check=_check_gauss)

    return res


__all__ = ['Bayes', 'bernoulli', 'categorical', 'binomial', 'multinomial', 'poisson', 'GaussianWishart',
           'gaussian']


if __name__ == '__main__':
    pass
