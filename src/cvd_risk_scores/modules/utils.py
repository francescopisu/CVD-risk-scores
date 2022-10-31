import logging
import numpy as np
import pandas as pd
from typing import Union

from src.config import settings
from src.cvd_risk_scores.modules import typings


class FraminghamPopulationStatistics:
    def __init__(self):
        self.__stats = {
            "female": {
                "prop": 0.532,
                "age": pd.DataFrame.from_dict({
                    "min": [30, 40, 50, 60],
                    "max": [40, 50, 60, 70], 
                    "prop": [0.3, 0.4, 0.20, 0.1]
                }),
                "SBP": pd.DataFrame.from_dict({
                    "min": [100, 125, 150], 
                    "max": [125, 150, 180], 
                    "prop": [0.2, 0.6, 0.20]
                }),
                "tch": pd.DataFrame.from_dict({
                    "min": [160, 190, 220], 
                    "max": [190, 220, 270], 
                    "prop": [0.6, 0.2, 0.20]
                }),            
                "HDL": pd.DataFrame.from_dict({
                    "min": [40, 50, 60], 
                    "max": [50, 60, 75], 
                    "prop": [0.3, 0.5, 0.20]
                }),
                "treated_for_BP": 0.118, # % over the 53.2%
                "smoking": 0.342,
                "diabetes": 0.038
            },
            "male": {
                "prop": 1 - 0.532,
                "age": pd.DataFrame.from_dict({
                    "min": [30, 40, 50, 60],
                    "max": [40, 50, 60, 70], 
                    "prop": [0.3, 0.4, 0.20, 0.1]
                }),
                "SBP": pd.DataFrame.from_dict({
                    "min": [100, 125, 150], 
                    "max": [125, 150, 180], 
                    "prop": [0.2, 0.6, 0.20]
                }),
                "tch": pd.DataFrame.from_dict({
                    "min": [160, 190, 220], 
                    "max": [190, 220, 270], 
                    "prop": [0.6, 0.2, 0.20]
                }),            
                "HDL": pd.DataFrame.from_dict({
                    "min": [30, 40, 50], 
                    "max": [40, 50, 65], 
                    "prop": [0.3, 0.5, 0.20]
                }),
                "treated_for_BP": 0.101, # % over the 53.2%
                "smoking": 0.352,
                "diabetes": 0.065
            },        
        }

    @property
    def stats(self):
        return self.__stats


def generate_population(n_sub: int = 1000, 
                        population_stats = None, 
                        random_state: Union[typings.Seed, np.random.Generator] = 1234):
    if not random_state:
        rng = np.random.default_rng(1234)
    elif not isinstance(random_state, np.random.Generator):
        rng = np.random.default_rng(random_state)
    else:
        rng = random_state
    
    pop_stats = FraminghamPopulationStatistics()

    population = pd.DataFrame(columns=["age", "sex", "SBP_nt", "SBP_t", "tch", "HDL", "smoking", "diabetes"])

    for sex, sex_stats in pop_stats.stats.items():
        # proportion of subjects of this sex
        n_sub_sex = round(sex_stats.pop("prop") * n_sub)

        sex_samplings = pd.DataFrame(columns=population.columns, index=range(n_sub_sex))

        # rng.choice(["male", "female"], n_sub_sex, replace=True, p=[var_stats, 1 - var_stats])
        sex_samplings["sex"] = [sex] * n_sub_sex

        # deal with proportion of subjects treated/not treated for BP
        treated = sex_stats.pop("treated_for_BP")

        # treated vs not treated boolean flags
        # we will use this to create SBP_nt and SBP_t
        # SBP_nt: zeros all the subjects who are under treatment for BP
        # SBP_t: zeros all the subjects who are not under treatment for BP
        treated_and_not_treated = rng.choice([True, False], n_sub_sex, replace=True, p=[treated, 1 - treated])
        
        # sample systolic blood pressures
        sbp_stats = sex_stats.pop("SBP")
        sbp_rows = rng.choice(range(len(sbp_stats["min"])), n_sub_sex, replace=True, p=sbp_stats["prop"])
        sbp_samplings = round(sbp_stats["min"][sbp_rows] + rng.uniform(low=0, high=1, size=n_sub_sex) * \
            (sbp_stats["max"][sbp_rows] - sbp_stats["min"][sbp_rows]))
        
        sex_samplings["SBP_nt"] = [sbp if not treated else 0 for treated, sbp in zip(treated_and_not_treated, sbp_samplings)]
        sex_samplings["SBP_t"] = [sbp if treated else 0 for treated, sbp in zip(treated_and_not_treated, sbp_samplings)]
        
        # deal with the rest of the variables
        for var, var_stats in sex_stats.items():
            if isinstance(var_stats, pd.DataFrame):
                # numerical variables
                rows = rng.choice(range(len(var_stats["min"])), n_sub_sex, replace=True, p=var_stats["prop"])
                dat = round(var_stats["min"][rows] + rng.uniform(low=0, high=1, size=n_sub_sex) * \
                     (var_stats["max"][rows] - var_stats["min"][rows])).values
                sex_samplings[var] = dat
            else:
                # categorical variables
                sex_samplings[var] = rng.choice([True, False], n_sub_sex, replace=True, p=[var_stats, 1 - var_stats])

        population = pd.concat([population, sex_samplings], axis=0)

        
    return population