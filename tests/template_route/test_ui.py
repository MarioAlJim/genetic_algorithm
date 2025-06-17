import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

configurations = [
    {"population_size": "4", "generations": "10", "selection_type": "random", "selection_rate": "0.5",
     "crossover_type": "one-point", "mutation_type": "random-resetting", "mutation_rate": "0.5", "elitism_rate": "0.5"},
    {"population_size": "8", "generations": "5", "selection_type": "steady-state", "selection_rate": "0.7",
     "crossover_type": "two-point", "mutation_type": "random-resetting", "mutation_rate": "0.3", "elitism_rate": "0.2"},
]

driver = webdriver.Edge()
driver.get("http://127.0.0.1:3000")

#initial config form
select_problem = Select(driver.find_element(By.ID, "problem_field"))
select_problem.select_by_value("triangle-classification")
select_algorithm = Select(driver.find_element(By.ID, "algorithm_field"))
select_algorithm.select_by_value("ga")
driver.find_element(By.ID, "initial_config_button").click()
time.sleep(2)

for config in configurations:
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

    # Send the config form
    driver.find_element(By.ID, "execute_algorithm_button").click()
    time.sleep(3)

    # validate results
    assert "div-results" in driver.page_source
    time.sleep(2)

# close the navigator
driver.quit()

