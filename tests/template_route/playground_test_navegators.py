import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


CONFIGURATIONS = [
    # PCU011
    {"population_size": "6", "generations": "10", "selection_type": "random",
     "selection_rate": "0.2", "crossover_type": "two-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.2", "elitism_rate": "0.1"},
    # PCU012
    {"population_size": "10", "generations": "10", "selection_type": "steady-state",
     "selection_rate": "0.6", "crossover_type": "one-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.6", "elitism_rate": "0.9"},
    # PCU013
    {"population_size": "3", "generations": "8", "selection_type": "random",
     "selection_rate": "0.3", "crossover_type": "one-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.5", "elitism_rate": "0.2"},
    # PCU014
    {"population_size": "7", "generations": "5", "selection_type": "steady-state",
     "selection_rate": "0.7", "crossover_type": "two-point",
     "mutation_type": "random-resetting", "mutation_rate": "0.1", "elitism_rate": "0.3"},
    # PCU015
    {"population_size": "9", "generations": "8", "selection_type": "steady-state",
     "selection_rate": "0.7", "crossover_type": "uniform",
     "mutation_type": "random-resetting", "mutation_rate": "0.6", "elitism_rate": "0.5"},
]


def run_tests(browser_name):
    if browser_name.lower() == "edge":
        driver = webdriver.Edge()
    elif browser_name.lower() == "chrome":
        driver = webdriver.Chrome()
    else:
        print(f"Browser {browser_name} is not supported.")
        return

    driver.get("http://127.0.0.1:5000")

    print(f"[{browser_name}] Initializing form...")
    select_problem = Select(driver.find_element(By.ID, "problem_field"))
    select_problem.select_by_value("triangle-classification")

    select_algorithm = Select(driver.find_element(By.ID, "algorithm_field"))
    select_algorithm.select_by_value("ga")

    driver.find_element(By.ID, "initial_config_button").click()
    time.sleep(2)

    results = []

    for idx, config in enumerate(CONFIGURATIONS, start=1):
        start = time.perf_counter()

        print(f"[{browser_name}] Executing PCU01{idx}...")

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

        duration = time.perf_counter() - start
        results.append((f"PCU01{idx}", duration))
        print(f"[{browser_name}] PCU01{idx} completed in {duration:.2f} seconds.\n")
        time.sleep(2)

    driver.quit()

    print(f"[{browser_name}] Summary of execution times:")
    for test_id, time_taken in results:
        print(f"[{browser_name}] {test_id}: {time_taken:.2f} seconds")


def main():
    """
    Test Concurrent petitions with different browsers.
    """
    # Create threads
    threads = []
    for browser in ["edge", "chrome"]:
        t = threading.Thread(target=run_tests, args=(browser,))
        t.start()
        threads.append(t)

    # Wait bot threads
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
