from info.basic.typehint import Numeric, T, Null
from info.basic.decorators import FuncTools
from info import docfunc as doc
from scipy.stats import chi2
import numpy as np
fun = __import__('info.basic.functions', fromlist=['_mvn_params'])
_mvn_params = getattr(fun, '_mvn_params')
_solve_cdf = getattr(fun, '_solve_cdf')
a = getattr(fun, 'hotelling_anomaly')
_matrix_duck = getattr(fun, '_matrix_like')


def hotelling_threshold(df: int, upper: Numeric, level: float = 0.05) -> float:
    """calculate the threshold of chi2 distribution, by a given test level"""
    dis = chi2(df=df)
    return _solve_cdf(dis.cdf, 1 - level, _range=[0, upper])


class Hotelling:

    @FuncTools.params_setting(data=T[Null: _matrix_duck], significance_level=T[0.05: lambda x: 0 <= x <= 1])
    def __init__(self, **params):
        self.settings = {k: v for k, v in params.items() if k in ['significance_level']}
        self.model, self.mean, self.sigma, self.threshold = [None for _ in range(4)]
        self.update(**params)

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def predict(self, **params):
        return self.predict_dissimilarity(data=params.get('data')) <= self.threshold

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def predict_dissimilarity(self, **params):
        return a(params.get('data'), self.mean, self.sigma)

    @FuncTools.params_setting(data=T[Null: _matrix_duck])
    def update(self, **params):
        self.model = np.vstack([self.model, params.get('data')]) if self.model is not None else params.get('data')
        self.mean, self.sigma = _mvn_params(self.model)
        self.threshold = hotelling_threshold(self.model.shape[1], self.model.shape[0],
                                             self.settings.get('significance_level'))


doc.redoc(Hotelling, doc.Hotelling)


if __name__ == '__main__':
    pass
