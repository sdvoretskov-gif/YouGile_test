from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__url = "https://ru.yougile.com/team/settings-account#ID-49"
        self.__driver = driver

    def go(self):
        self.__driver.get(self.__url)

    def login_as(self, email: str, password: str):
        # Ожидаем появления поля ввода логина
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='example@mail.ru']"))))
        (self.__driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='example@mail.ru']").
         clear())
        (self.__driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='example@mail.ru']").
         send_keys(email))

        # Ожидаем появления поля ввода пароля
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Введите пароль']"))))
        (self.__driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Введите пароль']").
         clear())
        (self.__driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Введите пароль']").
         send_keys(password))

        # Ожидаем появления логотипа
        # (убеждаемся что главная страница полностью загружена)
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "div[class='flex items-center justify-center gap-4']"))))
        (self.__driver.find_element(
            By.CSS_SELECTOR,
            "div[class='flex items-center justify-center gap-4']").
         click())

    def get_current_url(self):
        return self.__driver.current_url
