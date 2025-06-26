from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

class TestAbout:
    def test_open_about(self):
        driver = webdriver.Edge()
        driver.get("http://127.0.0.1:3000")
        driver.find_element(By.ID, "about_link").click()

        assert driver.current_url == "http://127.0.0.1:3000/about"
        driver.quit()

    def test_about_link_1(self):
        driver = webdriver.Edge()
        driver.get("http://127.0.0.1:3000")
        driver.find_element(By.ID, "about_link").click()
        driver.find_element(By.ID, "article_ref").click()

        assert driver.current_url == "https://ieeexplore.ieee.org/document/10795575"
        driver.quit()

    def test_about_link_2(self):
        driver = webdriver.Edge()
        driver.get("http://127.0.0.1:3000")
        driver.find_element(By.ID, "about_link").click()
        driver.find_element(By.ID, "repo_ref").click()

        assert driver.current_url == "https://github.com/MarioAlJim/genetic_algorithm"
        driver.quit()



