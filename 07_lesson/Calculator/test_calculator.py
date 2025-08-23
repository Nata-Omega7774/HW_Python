from CalcPage import CalcPage
import pytest
from selenium import webdriver

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_calculator(browser):
    delay = 45
    result = 15
    keys_press = '7+8='

    calc = CalcPage(browser)
    calc.open()
    calc.set_delay(delay)
    calc.input_text(keys_press)
    calc.wait_result(delay, result)

    assert calc.result_text() == str(result)