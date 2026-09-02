import allure
import pytest
from selenium import webdriver


@pytest.fixture(scope="function", autouse=True)
def browser():
    with allure.step("Открыть и настроить браузер"):
        browser = webdriver.Chrome()
        browser.implicitly_wait(4)
        browser.maximize_window()
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()
