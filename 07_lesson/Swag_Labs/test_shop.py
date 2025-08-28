from .Pages.LoginPage import LoginPage
from .Pages.ProductsPage import ProductsPage
from .Pages.CheckoutPage import CheckoutPage
import pytest
from selenium import webdriver

user_name = "standard_user"
password = "secret_sauce"

first_name = "Mark"
last_name = "Markov"
postal_code = "123456"

sum = "$58.29"

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_purchase(browser):
    login_page = LoginPage(browser)
    login_page.open()
    login_page.sign_in(user_name, password)

    products_page = ProductsPage(browser)
    products_page.add_to_cart()
    products_page.go_to_cart()
    products_page.checkout_click()

    checkout_page = CheckoutPage(browser)
    checkout_page.make_checkout(first_name, last_name, postal_code)

    txt = checkout_page.check_total()
    assert sum in txt
