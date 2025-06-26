import os
import shutil
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

DOWNLOAD_DIR = os.path.abspath("test_downloads")
@pytest.mark.parametrize("config", [
    {"population_size": "4", "generations": "10", "selection_type": "random", "selection_rate": "0.5",
     "crossover_type": "one-point", "mutation_type": "random-resetting", "mutation_rate": "0.5", "elitism_rate": "0.5"}
])

class TestDownload:

    @pytest.fixture(scope="module")
    def driver(self):
        """Configura el navegador con carpeta de descarga"""
        if os.path.exists(DOWNLOAD_DIR):
            shutil.rmtree(DOWNLOAD_DIR)
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        options = Options()
        options.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    def test_download_file(self, driver, config):
        """Download test Flask"""
        driver.get("http://localhost:3000/playground")

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

        download_button = driver.find_element(By.ID, "download-btn")
        download_button.click()

        expected_name = "Execution results.pdf"
        file = os.path.join(DOWNLOAD_DIR, expected_name)
        print(file)

        timeout = 15
        while timeout > 0:
            if os.path.exists(file):
                break
            time.sleep(1)
            timeout -= 1

        assert os.path.exists(file), "The file has not been downloaded."

    def test_download_file_2(self, driver, config):
        """Download test Flask"""
        driver.get("http://localhost:3000/playground")

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

        download_button = driver.find_element(By.ID, "download-btn")
        download_button.click()

        expected_name = "Execution results.pdf"
        file = os.path.join(DOWNLOAD_DIR, expected_name)
        print(file)

        timeout = 15
        while timeout > 0:
            if os.path.exists(file):
                break
            time.sleep(1)
            timeout -= 1

        assert os.path.exists(file), "The file has not been downloaded."

    def test_download_file_3(self, driver, config):
        """Download test Flask"""
        driver.get("http://localhost:3000/playground")

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

        download_button = driver.find_element(By.ID, "download-btn")
        download_button.click()

        assert "notification-container" in driver.page_source
