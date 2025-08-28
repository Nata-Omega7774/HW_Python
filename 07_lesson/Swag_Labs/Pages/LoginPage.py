from selenium.webdriver.common.by import By

Shop_URL = "https://www.saucedemo.com/"

class LoginPage:
    def __init__(self, browser, url=Shop_URL):
        self.browser = browser
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def sign_in(self, user_name, password):
        self.browser.find_element(By.CSS_SELECTOR, '#user-name').send_keys(user_name)
        self.browser.find_element(By.CSS_SELECTOR, '#password').send_keys(password)
        self.browser.find_element(By.CSS_SELECTOR, '#login-button').click()
