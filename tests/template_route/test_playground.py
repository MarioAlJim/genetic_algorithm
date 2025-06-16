# tests/test_form_e2e.py
"""End-to-end tests for the GA configuration form using Selenium."""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options


@pytest.fixture(scope="module")
def driver():
    """Initialize the Selenium WebDriver."""
    options = Options()
    options.add_argument("--headless")  # Remove this line if you want to see the browser
    service = EdgeService()
    driver_instance = webdriver.Edge(service=service, options=options)
    yield driver_instance
    driver_instance.quit()


def initialize_form(driver_instance):
    """Initialize the GA configuration form."""
    driver_instance.get("http://127.0.0.1:3000")

    select_problem = Select(driver_instance.find_element(By.ID, "problem_field"))
    select_problem.select_by_value("triangle-classification")

    select_algorithm = Select(driver_instance.find_element(By.ID, "algorithm_field"))
    select_algorithm.select_by_value("ga")

    driver_instance.find_element(By.ID, "initial_config_button").click()
    time.sleep(2)


@pytest.mark.parametrize("config", [
    # PCU011
    {
        "population_size": "6", "generations": "10", "selection_type": "random",
        "selection_rate": "0.2", "crossover_type": "two-point",
        "mutation_type": "random-resetting", "mutation_rate": "0.2", "elitism_rate": "0.1"
    },
    # PCU012
    {
        "population_size": "10", "generations": "10", "selection_type": "steady-state",
        "selection_rate": "0.6", "crossover_type": "one-point",
        "mutation_type": "random-resetting", "mutation_rate": "0.6", "elitism_rate": "0.9"
    },
    # PCU013
    {
        "population_size": "3", "generations": "8", "selection_type": "random",
        "selection_rate": "0.3", "crossover_type": "one-point",
        "mutation_type": "random-resetting", "mutation_rate": "0.5", "elitism_rate": "0.2"
    },
    # PCU014
    {
        "population_size": "7", "generations": "5", "selection_type": "steady-state",
        "selection_rate": "0.7", "crossover_type": "two-point",
        "mutation_type": "random-resetting", "mutation_rate": "0.1", "elitism_rate": "0.3"
    },
    # PCU015
    {
        "population_size": "9", "generations": "8", "selection_type": "steady-state",
        "selection_rate": "0.7", "crossover_type": "uniform",
        "mutation_type": "random-resetting", "mutation_rate": "0.6", "elitism_rate": "0.5"
    },
])
def test_valid_configurations(driver, config):
    """Test valid configurations from PCU011 to PCU015."""
    initialize_form(driver)

    driver.find_element(By.ID, "population_size_field").clear()
    driver.find_element(By.ID, "population_size_field").send_keys(config["population_size"])

    driver.find_element(By.ID, "generations_field").clear()
    driver.find_element(By.ID, "generations_field").send_keys(config["generations"])

    Select(driver.find_element(By.ID, "selection_type_field")).select_by_value(config["selection_type"])
    Select(driver.find_element(By.ID, "selection_rate_field")).select_by_value(config["selection_rate"])
    Select(driver.find_element(By.ID, "crossover_type_field")).select_by_value(config["crossover_type"])
    Select(driver.find_element(By.ID, "mutation_type_field")).select_by_value(config["mutation_type"])
    Select(driver.find_element(By.ID, "mutation_rate_field")).select_by_value(config["mutation_rate"])
    Select(driver.find_element(By.ID, "elite_pop_rate_field")).select_by_value(config["elitism_rate"])

    driver.find_element(By.ID, "execute_algorithm_button").click()
    time.sleep(4)

    assert "successful_execution" in driver.page_source


def test_default_configurations_pcu016(driver):
    """Test default configuration when no fields are modified (PCU016)."""
    initialize_form(driver)
    driver.find_element(By.ID, "execute_algorithm_button").click()
    time.sleep(4)

    assert "successful_execution" in driver.page_source


@pytest.mark.parametrize("config", [
    # PCU018 - Invalid population (too high)
    {
        "population_size": "51", "generations": "5", "selection_type": "steady-state",
        "selection_rate": "0.5", "crossover_type": "uniform",
        "mutation_type": "random-resetting", "mutation_rate": "0.8", "elitism_rate": "0.3"
    },
    # PCU0110 - Invalid population (negative), generations (zero)
    {
        "population_size": "-3", "generations": "0", "selection_type": "steady-state",
        "selection_rate": "0.5", "crossover_type": "uniform",
        "mutation_type": "random-resetting", "mutation_rate": "0.8", "elitism_rate": "0.3"
    },
    # PCU0111 - Invalid population (zero), generations (negative)
    {
        "population_size": "0", "generations": "-20", "selection_type": "steady-state",
        "selection_rate": "0.5", "crossover_type": "uniform",
        "mutation_type": "random-resetting", "mutation_rate": "0.8", "elitism_rate": "0.3"
    }
])
def test_invalid_configurations(driver, config):
    """Test invalid configurations from PCU018, PCU0110, and PCU0111."""
    initialize_form(driver)

    driver.find_element(By.ID, "population_size_field").clear()
    driver.find_element(By.ID, "population_size_field").send_keys(config["population_size"])

    driver.find_element(By.ID, "generations_field").clear()
    driver.find_element(By.ID, "generations_field").send_keys(config["generations"])

    Select(driver.find_element(By.ID, "selection_type_field")).select_by_value(config["selection_type"])
    Select(driver.find_element(By.ID, "selection_rate_field")).select_by_value(config["selection_rate"])
    Select(driver.find_element(By.ID, "crossover_type_field")).select_by_value(config["crossover_type"])
    Select(driver.find_element(By.ID, "mutation_type_field")).select_by_value(config["mutation_type"])
    Select(driver.find_element(By.ID, "mutation_rate_field")).select_by_value(config["mutation_rate"])
    Select(driver.find_element(By.ID, "elite_pop_rate_field")).select_by_value(config["elitism_rate"])

    driver.find_element(By.ID, "execute_algorithm_button").click()
    time.sleep(1)

    assert "is-invalid" in driver.page_source or "error" in driver.page_source
