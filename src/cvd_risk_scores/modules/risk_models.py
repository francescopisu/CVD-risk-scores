import abc
import numpy as np
import pandas as pd
from functools import partial
from pydantic import validate_arguments, Field
from pydantic.typing import Annotated
from typing import List, Tuple, Optional, Dict

from .typings import ArrayLike
from .templates import FraminghamSubject, BaseSubject

class RiskModel(abc.ABC):
    """
    The risk model base class. It is based upon the pytorch paradigm with a forward method that implements
    the computation.  When the class is called via the `__call__` method, the `forward` method is invoked.

    Methods
    ----------
    _compute_single(self, subject):
        an abstract method for computing the score for a single subject that must be 
        implemented in each custom risk model. 
    """
    @abc.abstractmethod
    def _compute_single(self, subject: BaseSubject) -> float:
        pass

    def _compute_single_from_slice(self, aslice: ArrayLike, columns: List[str], indexes: List[int]) -> float:
        """Takes a slice of an array and computes the risk.

        Parameters
        ----------
        aslice : ArrayLike
            A slice of an array of covariates
        columns : List[str]
            List of covariate names
        indexes : List[int]
            List of covariate indexes in the slice

        Returns
        -------
        float
            The risk score
        """
        sub = self.template(**dict(zip(columns, aslice[indexes])))
        return self.fn(sub)

    def forward(self, data: ArrayLike, columns_map: Dict[str, str] = None) -> ArrayLike:
        """
        Computes risk scores for each subject in the `data` array - i.e., a row -
        and for the specified `columns` in a specific order (i.e., `indexes`).

        Example:
        --------
        Suppose we need `age`, `sex` and `HDL` for computing the score.
        Suppore that we also have other columns in a data array like the following:

        age | cov1 | sex | cov2 | HDL

        Then, we would specificy the following variables:
        `columns_map = {
            "age": "age",
            "cov1: "cov1",
            "sex": "sex",
            "cov2: "cov2",
            "HDL": "HDL"
        }

        Parameters:
        -----------
        data: ArrayLike
            the data array cointaining a subject in each row
        columns_map: Dict[str, str]
            A dictionary defining the mapping between the user's columns
            necessary to compute the score and the expected columns
            from the FraminghamRiskScore model. 
            If data is either a list of lists or a numpy array,
            the keys of this dictionary must be in the correct order
            so that data can be cast into a pandas DataFrame.
        
        Returns:
        --------
        ArrayLike
            an array of scores, one for each subject
        """
        if not isinstance(columns_map, dict):
            raise ValueError("columns_map must be a dictionary mapping your column names to the \
                             expected columns.")
        if not isinstance(data, pd.DataFrame) and isinstance(data, (list, np.ndarray)):
            data = pd.DataFrame(data=data, columns=list(columns_map.keys()))

        indexes = [data.columns.get_loc(c) for c in columns_map.keys()]

        scores = np.apply_along_axis(partial(self._compute_single_from_slice, 
                                             columns=list(columns_map.values()),
                                             indexes=indexes), 
                                   axis=1, 
                                   arr=data)
        
        return scores        

    def __call__(self, *args, **kwargs):
        out = self.forward(*args, **kwargs)

        return out


class FraminghamRiskScore(RiskModel):
    """
    This class implements the 10-y Framingham

    Examples:
    ------
    >>> # data = <YOUR DATA> # either a pandas Dataframe, a numpy array or a list of lists
    >>> frs = FraminghamRiskScore()
    >>> columns_map = {
    >>>    "sex": "sex",
    >>>    "age": "age",
    >>>    "SBP_nt": "SBP_nt",
    >>>    "SBP_t": "SBP_t",
    >>>    "tch": "tch",
    >>>    "HDL": "HDL",
    >>>    "smoking": "smoking",
    >>>    "diabetes": "diabetes"
    >>> }
    >>> scores = frs(data, columns_map=columns_map)

    References:
    -----------
    [1] D'Agostino, Ralph B Sr et al. “General cardiovascular risk profile for use in primary care: 
    the Framingham Heart Study.” Circulation vol. 117,6 (2008): 743-53. doi:10.1161/CIRCULATIONAHA.107.699579
    """
    def __init__(self):
        self.baseline_risk = {"female": 0.95012, "male": 0.88936}
        self.mean_risk = {"female": 26.1931, "male": 23.9802}
        self.betas = {
            "female": {
                "age": 2.32888,
                "tch": 1.20904,
                "HDL": -0.70833,
                "SBP_nt": 2.76157,
                "SBP_t": 2.82263,
                "smoking": 0.52873,
                "diabetes": 0.69154
            },
            "male": {
                "age": 3.06117,
                "tch": 1.12370,
                "HDL": -0.93263,
                "SBP_nt": 1.93303,
                "SBP_t": 1.99881,
                "smoking": 0.65451,
                "diabetes": 0.57367
            }
        }
        self.fn = self._compute_single
        self.template = FraminghamSubject
    

    @validate_arguments
    def _compute_single(self, subject: FraminghamSubject) -> float:
        """Compute the risk score for a single subject

        Parameters
        ----------
        subject : FraminghamSubject
            The subject to compute the risk score for

        Returns
        -------
        float
            The Framingham risk score for this subject
        """
        sex = subject.sex

        lin_comb = 0
        for param, beta in self.betas[sex].items():
            curr_val = getattr(subject, param)
            if isinstance(curr_val, (int, float)) and (not isinstance(curr_val, bool) and curr_val != 0):
                curr_val = np.log(curr_val)

            lin_comb += curr_val * beta

        return 1 - np.power(self.baseline_risk[sex], np.exp(lin_comb - self.mean_risk[sex]))