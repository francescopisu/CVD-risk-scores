import numpy as np
import pandas as pd
import pytest
import logging

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
def numpy_array(male_subject, female_subject):
    return np.array([list(male_subject.values()), list(female_subject.values())])

@pytest.fixture
def pandas_df():
    columns = ['Cov1', 'TotalChol', 'HDL', 'CovX', 'DIABETES', 'Cov2', 'TREATBP', 'SBP_nt', 
               'SBP_t', 'Cov3', 'gender', 'age', 'smoker', 'Cov4']
    
    data = [99, 160, 48, "yes", True, 451, False, 0.0, 146.0, 'no', 'female', 65, False, 0.05]

    df = pd.DataFrame(data=[data], columns=columns)
    return df

@pytest.fixture
def list_of_lists(male_subject, female_subject):
    return [list(male_subject.values()), list(female_subject.values())]

@pytest.fixture
def framingham_col_map1():
    col_map = {
        "age": "age",
        "gender": "sex",
        "SBP_nt": "SBP_nt",
        "SBP_t": "SBP_t",
        "TotalChol": "tch",
        "HDL": "HDL",
        "smoker": "smoking",
        "DIABETES": "diabetes"
    }

    return col_map

@pytest.fixture
def framingham_col_map2():
    col_map = {
        "sex": "sex",
        "age": "age",
        "SBP_nt": "SBP_nt",
        "SBP_t": "SBP_t",
        "tch": "tch",
        "HDL": "HDL",
        "smoking": "smoking",
        "diabetes": "diabetes"
    }

    return col_map


def test_framingham_risk_score(numpy_array, pandas_df, list_of_lists, framingham_col_map1, framingham_col_map2):
    frs = FraminghamRiskScore()

    with pytest.raises(ValueError) as ve:
        frs(numpy_array, 
            columns_map=["sex", "age", "SBP_nt", "SBP_t", "tch", "HDL", "smoking", "diabetes"])

    scores1 = frs(numpy_array, columns_map=framingham_col_map2)
    assert np.allclose(scores1, [0.1562, 0.1048], atol=0.0001)
    
    scores2 = frs(list_of_lists, columns_map=framingham_col_map2)
    assert np.allclose(scores2, [0.1562, 0.1048], atol=0.0001)

    scores3 = frs(pandas_df, columns_map=framingham_col_map1)
    assert np.allclose(scores3, [0.2402], atol=0.0001)
