"""Concurrent execution of GA config tests using Selenium and threading."""

import time
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

CONFIGURATIONS = [
    # PCU011 to PCU015
    {"population_size": "6", "generations": "10", "selection_type": "random",
     "selection_rate": "0.2", "crossover_type": "two-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.2", "elitism_rate": "0.1"},
    {"population_size": "10", "generations": "10", "selection_type": "steady-state",
     "selection_rate": "0.6", "crossover_type": "one-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.6", "elitism_rate": "0.9"},
    {"population_size": "3", "generations": "8", "selection_type": "random",
     "selection_rate": "0.3", "crossover_type": "one-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.5", "elitism_rate": "0.2"},
    {"population_size": "7", "generations": "5", "selection_type": "steady-state",
     "selection_rate": "0.7", "crossover_type": "two-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.1", "elitism_rate": "0.3"},
    {"population_size": "9", "generations": "8", "selection_type": "steady-state",
     "selection_rate": "0.7", "crossover_type": "uniform",
     "mutation_type": "random-resetting", "mutation_rate": "0.6", "elitism_rate": "0.5"},
]


def create_driver():
    """Create a headless Chrome WebDriver instance."""
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=ChromeService(), options=options)

barrier = threading.Barrier(len(CONFIGURATIONS))

def execute_test(config, test_id):
    """Execute a GA form submission with the given configuration."""
    driver = create_driver()
    try:
        barrier.wait()

        driver.get("http://127.0.0.1:3000")
        select_problem = Select(driver.find_element(By.ID, "problem_field"))
        select_problem.select_by_value("triangle-classification")

        select_algorithm = Select(driver.find_element(By.ID, "algorithm_field"))
        select_algorithm.select_by_value("ga")

        driver.find_element(By.ID, "initial_config_button").click()
        time.sleep(1)

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
        time.sleep(3)

        assert "successful_execution" in driver.page_source
        print(f"[{test_id}] Success.")

    except Exception as err:
        print(f"[{test_id}] Failed: {err}")
    finally:
        driver.quit()


def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for idx, config in enumerate(CONFIGURATIONS, start=1):
            test_id = f"PCU01{idx}"
            future = executor.submit(execute_test, config, test_id)
            futures.append(future)
        wait(futures)


if __name__ == "__main__":
    main()
