"""Concurrent performance test of GA configurations using Selenium and CSV export."""

import csv
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

CONFIGURATIONS = [
    {"id": "PCU011", "population_size": "6", "generations": "10", "selection_type": "random",
     "selection_rate": "0.2", "crossover_type": "two-point", "mutation_type": "random-resetting",
     "mutation_rate": "0.2", "elitism_rate": "0.1"},
    {"id": "PCU012", "population_size": "10", "generations": "10", "selection_type": "steady-state",
     "selection_rate": "0.6", "crossover_type": "one-point", "mutation_type": "random-resetting",
     "mutation_rate": "0.6", "elitism_rate": "0.9"},
    {"id": "PCU013", "population_size": "3", "generations": "8", "selection_type": "random",
     "selection_rate": "0.3", "crossover_type": "one-point", "mutation_type": "random-resetting",
     "mutation_rate": "0.5", "elitism_rate": "0.2"},
    {"id": "PCU014", "population_size": "7", "generations": "5", "selection_type": "steady-state",
     "selection_rate": "0.7", "crossover_type": "two-point", "mutation_type": "random-resetting",
     "mutation_rate": "0.1", "elitism_rate": "0.3"},
    {"id": "PCU015", "population_size": "9", "generations": "8", "selection_type": "steady-state",
     "selection_rate": "0.7", "crossover_type": "uniform", "mutation_type": "random-resetting",
     "mutation_rate": "0.6", "elitism_rate": "0.5"},
]


def create_driver():
    """Create a headless Chrome WebDriver instance."""
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=ChromeService(), options=options)


def fill_form(driver, config):
    """Fill the form with GA configuration values."""
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


def execute_test(config):
    """Run a single GA configuration test and return result."""
    driver = create_driver()
    result = {"id": config["id"], "status": "failed", "duration": None}

    try:
        driver.get("http://127.0.0.1:5000")
        wait = WebDriverWait(driver, 10)

        Select(driver.find_element(By.ID, "problem_field")).select_by_value("triangle-classification")
        Select(driver.find_element(By.ID, "algorithm_field")).select_by_value("ga")
        driver.find_element(By.ID, "initial_config_button").click()

        wait.until(EC.visibility_of_element_located((By.ID, "population_size_field")))

        start = time.perf_counter()

        fill_form(driver, config)
        driver.find_element(By.ID, "execute_algorithm_button").click()

        wait.until(EC.presence_of_element_located((By.ID, "div-results")))

        result["duration"] = round(time.perf_counter() - start, 2)
        result["status"] = "success"

        print(f"[{config['id']}] Success in {result['duration']}s")

    except Exception as err:
        print(f"[{config['id']}] Error: {err}")
    finally:
        driver.quit()

    return result


def save_results_to_csv(results, filename="performance_results.csv"):
    """Save execution results to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "status", "duration"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def main():
    """Execute all GA configuration tests concurrently and store results."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(execute_test, CONFIGURATIONS))

    print("\nFinal summary:")
    for res in results:
        print(f"{res['id']}: {res['status']} - {res['duration']}s")

    save_results_to_csv(results)
    print("Results saved to 'performance_results.csv'")


if __name__ == "__main__":
    main()
