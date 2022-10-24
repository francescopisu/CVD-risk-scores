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
  "sex": "female",
  "age": 61,
  "SBP_nt": 124,
  "SBP_t": 0,
  "tch": 180,
  "HDL": 47,
  "smoking": True,
  "diabetes": False
}

# Create a numpy array from features values
data = np.array([list(subject.values())])

# Alternatively:
#data = np.array([
#  ["female", 61, 124, 0, 180, 47, True, False]
#])

# Define the columns required by the Framingham risk score in the correct order
# depending on how the data at the previous step was defined
columns = list(subject.keys())

# Alternatively:
#columns = ["sex", "age", "SBP_nt", "SBP_t", "tch", "HDL", "smoking", "diabetes"]

# Define the indexes of these columns in the data array
indexes = list(range(len(data.shape[1]))) # if the specified columns are contiguous in the data array

# Alternatively, you can specify the exact position of each column in case
# some aren't relevant for computing the chosen risk model
# indexes = [0, 2, 3, 4, 6, etc..]

# Compute the risk score
risk_score = risk_model(data=data, columns=columns, indexes=indexes)
```

## About

`CVD-risk-scores` is a Python package for computing cardiovascular disease risk using clinically validated models. It exposes an object-based API for interacting with risk models that is inspired by the `torch` paradigm of callable objects.

Available risk models:
* Framingham Risk Score
