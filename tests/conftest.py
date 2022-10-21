import numpy as np
import pandas as pd
import pytest

from cvd_risk_scores.config import settings

@pytest.fixture
def rng() -> np.random.Generator:
    """Construct a new Random Generator using the seed specified in settings.

    Returns:
        numpy.random.Generator: a Random Generator based on BitGenerator(PCG64)
    """
    return np.random.default_rng(settings.SEED)

