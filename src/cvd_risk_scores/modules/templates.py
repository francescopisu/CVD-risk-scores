from enum import Enum
# from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic.typing import Annotated

class Sex(Enum):
    MALE = "male"
    FEMALE = "female"


class BaseSubject(BaseModel):
    class Config:
        use_enum_values = True
        
    @classmethod
    def get_field_names(cls, alias=False):
        return list(cls.schema(alias).get("properties").keys())


class FraminghamSubject(BaseSubject):
    """
    Subject template for the Framingham risk score.

    Attributes:
    -----------
    sex : Sex
        Sex of subject.
    age : int
        Age in years.
    HDL : float
        High-density lipoprotein.
    tch : float
        Total cholesterol.
    SBP_nt : float
        Systolib blood pressure, not treated.
    SBP_t : float
        Systolic blood pressure, treated.
    smoking : bool
        Is smoker.
    diabetes : bool
        Is diabetic.
    """
    sex : Sex
    age : Annotated[float, Field(gt=30.0)]
    HDL : float
    tch : float
    SBP_nt : float
    SBP_t : float
    smoking : bool
    diabetes : bool