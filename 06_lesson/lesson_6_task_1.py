from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Перейти на страницу
driver.implicitly_wait(30)
driver.get("http://www.uitestingplayground.com/ajax")

# Найти элемент и кликнуть
driver.find_element(By.CSS_SELECTOR, "#ajaxButton").click()

# Изменить название кнопки
content = driver.find_element(By.CSS_SELECTOR, "#content")
txt = content.find_element(By.CSS_SELECTOR, "p.bg-success").text

# вывести в консоль
print(txt)

driver.quit()