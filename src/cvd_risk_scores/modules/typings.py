import numpy
import random
import sys
from typing import Union

try:
    from numpy.typing import ArrayLike
except ImportError:
    ArrayLike = Union[numpy.ndarray, List[List[float]]]

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

Seed: TypeAlias = Union[int, random.seed, numpy.random.seed]


