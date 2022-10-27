[![CircleCI](https://circleci.com/gh/francescopisu/CVD-risk-scores.svg?style=shield)](https://circleci.com/gh/francescopisu/CVD-risk-scores)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# CVD-risk-scores
A Python package for computing cardiovascular disease risk using clinically validated models.

Note: **This is a work in progress**

## Install
This package is available on PyPI
```bash
pip install cvd-risk-scores
```

## Getting started

`CVD-risk-scores` is based upon the `torch` philosophy of callable objects. Each `RiskModel` subclass is a callable upon 
initialisation, taking an array-like of subjects, each defined by some variables of interest, and returning an array-like of `float` values corresponding to cardiovascular risk scores.

```python
import cvd_risk_scores

# Instantiate the risk model we are interested in
risk_model = cvd_risk_scores.FraminghamRiskScore()

# Define our subject, in this case using a dictionary
subject = {
  "gender": "female",
  "age": 61,
  "SBP_nt": 124,
  "SBP_t": 0,
  "TotalChol": 180,
  "HDL": 47,
  "smoker": True,
  "diabetes": False
}

# Create a numpy array from features values
data = np.array([list(subject.values())])

# Alternatively:
#data = np.array([
#  ["female", 61, 124, 0, 180, 47, True, False]
#])

# define a dictionary mapping our own column names to the names
# expected by the risk score model.
# if data is either a numpy array or a list of lists,
# the `columns_map` mapping must present the columns
# in the correct order so that data can be cast to a pandas DataFrame.
columns_map = {
  "gender": "sex",
  "age": "age",
  "SBP_nt": "SBP_nt",
  "SBP_t": "SBP_t",
  "TotalChol": "tch",
  "HDL": "HDL",
  "smoker": "smoking",
  "diabetes": "diabetes"
}

# Compute the risk score
risk_score = risk_model(data=data, columns_map=columns_map)
```

## About

`CVD-risk-scores` is a Python package for computing cardiovascular disease risk using clinically validated models. It exposes an object-based API for interacting with risk models that is inspired by the `torch` paradigm of callable objects.

Available risk models:
* Framingham Risk Score


## References
[1] D'Agostino, Ralph B Sr et al. “General cardiovascular risk profile for use in primary care: 
the Framingham Heart Study.” Circulation vol. 117,6 (2008): 743-53. doi:10.1161/CIRCULATIONAHA.107.699579