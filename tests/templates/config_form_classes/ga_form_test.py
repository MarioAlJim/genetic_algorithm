# tests/test_forms.py
from ga_configurations_form import GAConfigurationsForm

def test_form_valid_case_pcu011(test_app):
    """PCU011 """
    form = GAConfigurationsForm(data={
        'population_size': 6,
        'generations': 10,
        'selection_type': 'random',
        'selection_rate': "0.2",
        'crossover_type': 'two-point',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.2",
        'elite_pop_rate': "0.1"
    })
    assert form.validate() is True

def test_form_valid_case_pcu012(test_app):
    """PCU012 """
    form = GAConfigurationsForm(data={
        'population_size': 10,
        'generations': 10,
        'selection_type': 'steady-state',
        'selection_rate': "0.6",
        'crossover_type': 'one-point',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.6",
        'elite_pop_rate': "0.9"
    })
    assert form.validate() is True

def test_form_valid_case_pcu013(test_app):
    """PCU013 """
    form = GAConfigurationsForm(data={
        'population_size': 3,
        'generations': 8,
        'selection_type': 'random',
        'selection_rate': "0.3",
        'crossover_type': 'one-point',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.5",
        'elite_pop_rate': "0.2"
    })
    assert form.validate() is True

def test_form_valid_case_pcu014(test_app):
    """PCU014 """
    form = GAConfigurationsForm(data={
        'population_size': 7,
        'generations': 5,
        'selection_type': 'steady-state',
        'selection_rate': "0.7",
        'crossover_type': 'two-point',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.1",
        'elite_pop_rate': "0.3"
    })
    assert form.validate() is True

def test_form_valid_case_pcu015(test_app):
    """PCU015"""
    form = GAConfigurationsForm(data={
        'population_size': 9,
        'generations': 8,
        'selection_type': 'steady-state',
        'selection_rate': "0.7",
        'crossover_type': 'uniform',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.6",
        'elite_pop_rate': "0.5"
    })
    assert form.validate() is True

# tests/test_forms.py
"""Test suite for GAConfigurationsForm - cases PCU016 to PCU0111."""

def test_form_defaults_pcu016(test_app):
    """PCU016/PCU017: Validate default configuration values."""
    form = GAConfigurationsForm()
    assert form.population_size.data == 5
    assert form.generations.data == 5
    assert form.selection_rate.data == "0.5"
    assert form.mutation_rate.data == "0.5"
    assert form.elite_pop_rate.data == "0.5"

def test_form_invalid_population_above_max(test_app):
    """PCU018: Invalid - population size exceeds maximum allowed value."""
    form = GAConfigurationsForm(data={
        'population_size': 51,
        'generations': 5,
        'selection_type': 'steady-state',
        'selection_rate': "0.5",
        'crossover_type': 'uniform',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.8",
        'elite_pop_rate': "0.3"
    })
    assert not form.validate()
    assert 'population_size' in form.errors

def test_form_invalid_generation_above_max(test_app):
    """PCU019: Invalid - number of generations exceeds max allowed."""
    form = GAConfigurationsForm(data={
        'population_size': 8,
        'generations': 101,
        'selection_type': 'steady-state',
        'selection_rate': "0.5",
        'crossover_type': 'uniform',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.8",
        'elite_pop_rate': "0.3"
    })
    assert not form.validate()
    assert 'generations' in form.errors

def test_form_invalid_negative_population_and_zero_generation(test_app):
    """PCU0110: Invalid - negative population and zero generations."""
    form = GAConfigurationsForm(data={
        'population_size': -3,
        'generations': 0,
        'selection_type': 'steady-state',
        'selection_rate': "0.5",
        'crossover_type': 'uniform',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.8",
        'elite_pop_rate': "0.3"
    })
    assert not form.validate()
    assert 'population_size' in form.errors
    assert 'generations' in form.errors

def test_form_invalid_zero_population_and_negative_generation(test_app):
    """PCU0111: Invalid - zero population and negative generations."""
    form = GAConfigurationsForm(data={
        'population_size': 0,
        'generations': -20,
        'selection_type': 'steady-state',
        'selection_rate': "0.5",
        'crossover_type': 'uniform',
        'mutation_type': 'random-resetting',
        'mutation_rate': "0.8",
        'elite_pop_rate': "0.3"
    })
    assert not form.validate()
    assert 'population_size' in form.errors
    assert 'generations' in form.errors

def test_form_reload_defaults_pcu0112(test_app):
    """PCU0112: Validate default values are reset after page reload."""
    form = GAConfigurationsForm()
    assert form.population_size.data == 5
    assert form.generations.data == 5
    assert form.selection_rate.data == "0.5"
    assert form.mutation_rate.data == "0.5"
    assert form.elite_pop_rate.data == "0.5"
