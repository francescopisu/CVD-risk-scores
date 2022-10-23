import numpy as np
import pytest

from src.cvd_risk_scores.modules import FraminghamRiskScore

@pytest.fixture
def female_subject():
    return {
        "sex": "female",
        "age": 61,
        "SBP_nt": 124,
        "SBP_t": 0,
        "tch": 180,
        "HDL": 47,
        "smoking": True,
        "diabetes": False
    }

@pytest.fixture
def male_subject():
    return {
        "sex": "male",
        "age": 53,
        "SBP_nt": 0,
        "SBP_t": 125,
        "tch": 161,
        "HDL": 55,
        "smoking": False,
        "diabetes": True
    }

@pytest.fixture
def col_order_idxs():
    columns = ["sex", "age", "SBP_nt", "SBP_t", "tch", "HDL", "smoking", "diabetes"]
    return (columns, list(range(len(columns))))


@pytest.fixture
def data_array(male_subject, female_subject):
    return np.array([list(male_subject.values()), list(female_subject.values())])


def test_framingham_risk_score(data_array, col_order_idxs):
    frs = FraminghamRiskScore()
    scores = frs(data_array, 
                 columns=col_order_idxs[0],
                 indexes=col_order_idxs[1])

    assert np.allclose(scores, [0.1562, 0.1048], atol=0.0001)