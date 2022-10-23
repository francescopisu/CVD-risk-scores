import abc
import numpy as np
from functools import partial
from pydantic import validate_arguments, Field
from pydantic.typing import Annotated
from typing import List, Tuple

from .typings import ArrayLike
from .templates import FraminghamSubject

class RiskModel(abc.ABC):
    """
    The risk model base class. It is based upon the pytorch paradigm with a forward method that implements
    the computation.

    Methods
    ----------
    forward(self, *args, **kwargs):
        an abstract method that each custom risk model must implement. 
        When the class is called via the `__call__` method, the `forward` method is invoked.
    """
    
    @abc.abstractmethod
    def forward(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        out = self.forward(*args, **kwargs)

        return out


class FraminghamRiskScore(RiskModel):
    """
    This class implements the 10-y Framingham

    Examples:
    ------
    >>> # data = <YOUR DATA>
    >>> frs = FraminghamRiskScore()
    >>> columns = ["sex", "age", "SBP_nt", "SBP_t", "tch", "HDL", "smoking", "diabetes"]
    >>> indexes = [0, 1, 2, 3, 4, 5, 6, 7]
    >>> scores = frs(data, columns=columns, indexes=indexes)

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
        self.fn = self.__compute_single
        self.template = FraminghamSubject
    

    @validate_arguments
    def __compute_single(self, subject: FraminghamSubject) -> float:
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

    
    def forward(self, data: ArrayLike, columns: List[str], indexes: List[int]) -> ArrayLike:
        """
        Computes risk scores for each subject in the `data` array - i.e., a row -
        and for the specified `columns` in a specific order (i.e., `indexes`).

        Example:
        --------
        Suppose we need `age`, `sex` and `HDL` for computing the score.
        Suppore that we also have other columns in a data array like the following:

        age | SBP_nt | sex | smoking | HDL

        Then, we would specificy the following variables:
        `columns = ["age", "sex", "HDL"]`
        `indexes = [0, 2, 4]`

        Parameters:
        -----------
        data: ArrayLike
            the data array cointaining a subject in each row
        columns: List[str]
            The list of columns that will be used to compute the score
        indexes: List[int]
            Indexes of the columns that will be used to compute the score
        
        Returns:
        --------
        ArrayLike
            an array of scores, one for each subject
        """
        def compute_single_from_slice(aslice, columns: List[str], indexes: List[int]) -> float:
            sub = self.template(**dict(zip(columns, aslice[indexes])))
            return self.fn(sub)

        scores = np.apply_along_axis(partial(compute_single_from_slice, 
                                             columns=columns,
                                             indexes=indexes), 
                                   axis=1, 
                                   arr=data)
        
        return scores