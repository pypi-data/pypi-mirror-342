# TODO: can model_lightweight attribute be used for all algorithm?
# if so, support queue obj for online learning


from .hotelling import Hotelling
from .nbayes import NaiveBayes
from .nearest import Neighbors
from .directional import VonMisesFisher


__all__ = ['Hotelling', 'NaiveBayes', 'Neighbors', 'VonMisesFisher']
