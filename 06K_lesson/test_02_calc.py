from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService
(ChromeDriverManager().install()))


def test_form_calculator():
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
    driver.implicitly_wait(5)
    driver.maximize_window()

    input_delay = driver.find_element(By.ID, "delay")
    input_delay.clear()
    input_delay.send_keys('45')
    sleep(1)
    driver.find_element(By.XPATH, '//span[contains(text(),"7")]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//span[contains(text(),"+")]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//span[contains(text(),"8")]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//span[contains(text(),"=")]').click()
    sleep(1)
    WebDriverWait(driver, "46").until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.screen"), "15"))

    assert driver.find_element(By.CSS_SELECTOR, "div.screen").text == "15"

    sleep(3)

    driver.quit()