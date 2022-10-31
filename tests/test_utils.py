import pytest

from src.cvd_risk_scores.modules import utils

@pytest.mark.parametrize('n_sub', [100, 1000])
@pytest.mark.parametrize('population_stats', [utils.FraminghamPopulationStatistics])
def test_generate_framingham(n_sub, population_stats, rng):
    pop_stats = population_stats()
    population = utils.generate_population(n_sub, pop_stats, random_state=rng)
    
    assert population.shape[0] == n_sub
    assert population.query("sex == 'female'").shape[0] == round(n_sub * pop_stats.stats.get("female").get("prop"))
    assert population.query("sex == 'male'").shape[0] == round(n_sub * pop_stats.stats.get("male").get("prop"))