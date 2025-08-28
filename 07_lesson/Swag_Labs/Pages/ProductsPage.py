from selenium.webdriver.common.by import By


class ProductsPage:
    def __init__(self, browser):
        self.browser = browser

    def add_to_cart(self):
        self.browser.find_element(By.CSS_SELECTOR, '#add-to-cart-sauce-labs-backpack').click()
        self.browser.find_element(By.CSS_SELECTOR, '#add-to-cart-sauce-labs-bolt-t-shirt').click()
        self.browser.find_element(By.CSS_SELECTOR, '#add-to-cart-sauce-labs-onesie').click()

    def go_to_cart(self):
        self.browser.find_element(By.CSS_SELECTOR, '.shopping_cart_link').click()

    def checkout_click(self):
        self.browser.find_element(By.CSS_SELECTOR, '#checkout').click()
