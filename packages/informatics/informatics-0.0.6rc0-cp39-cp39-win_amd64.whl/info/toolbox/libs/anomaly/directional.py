from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null
from info import docfunc as doc
from numpy import ndarray
import numpy as np
from scipy.stats import chi2, vonmises_fisher
fun = __import__('info.basic.functions', fromlist=['unitize'])
unitize = getattr(fun, 'unitize')
miu = getattr(fun, '_miu')
a = getattr(fun, 'directional_anomaly')
_moment_2_origin = getattr(fun, '_moment_2_origin')
_chi2_params = getattr(fun, '_chi2_params')
_solve_cdf = getattr(fun, '_solve_cdf')
_matrix_duck = getattr(fun, '_matrix_like')


class VonMisesFisher:

    @FuncTools.params_setting(data=T[Null: _matrix_duck], significance_level=T[0.05: lambda x: 0 <= x <= 1])
    def __init__(self, **params):
        self.settings = {k: v for k, v in params.items() if k in ['significance_level']}
        self.model, self.mean, self.m, self.s, self.a, self.threshold, self.dis = [None for _ in range(7)]
        self.update(**params)

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def predict(self, **params):
        return self.predict_dissimilarity(data=params.get('data')) <= self.threshold

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def predict_dissimilarity(self, **params):
        return a(params.get('data'), self.mean)

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def update(self, **params):
        self.model = np.vstack([self.model, params.get('data')]) if self.model is not None else params.get('data')
        self.mean = miu(self.model)
        self.a = a(self.model, self.mean)
        self.threshold = self._chi2_threshold(self.model, self.settings.get('significance_level'))
        self.dis = vonmises_fisher(self.mean, (0.5/self.s))

    def _chi2_threshold(self, x: ndarray, level: float = 0.05) -> float:
        """calculate the threshold of chi2 distribution, by a given significance level"""
        self.m, self.s = _chi2_params(a(x, miu(x)))
        chi2_dis = chi2(df=self.m, scale=self.s)
        return _solve_cdf(chi2_dis.cdf, 1 - level, _range=[0, 1])


doc.redoc(VonMisesFisher, doc.VonMisesFisher)


if __name__ == '__main__':
    pass
