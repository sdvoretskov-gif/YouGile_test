import pytest
import uuid
import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from YouGile.page.AuthPageUI import AuthPage
from YouGile.page.CompanyPageUI import CompanyPage
import os
from dotenv import load_dotenv


load_dotenv()

pytestmark = [pytest.mark.ui]

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


@allure.epic("YouGile UI")
@allure.story("Логирование")
@allure.title("Логирование")
def test_auth(browser):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    with allure.step("Проверить текущий url"):
        cur_url = auth_page.get_current_url()
        assert cur_url == "https://ru.yougile.com/team"


@allure.epic("YouGile UI")
@allure.story("Страница проектов")
@allure.title("Переход на страницу проектов")
def test_company_page(browser):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
    comp_page.current_url()
    with allure.step("Убедиться что находишься на страницы своей компании"):
        comp_page.company_name()
    with allure.step(
            "Дополнительно проверить нахождения на странице "
            "своей компании по URL"):
        actual_url = comp_page.current_url()
    assert actual_url == 'https://ru.yougile.com/team/projects', \
        (f"Тест НЕ пройден. Ожидался полный URL {actual_url}, "
         f"но получен другой")


@allure.epic("YouGile UI")
@allure.story("Создание проекта")
@allure.title("Создание проекта")
def test_create_project(browser, timeout=None):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
    project_name = f"Skyeng_{uuid.uuid4().hex[:6]}"
    with allure.step(f"Создать проект '{project_name}'"):
        comp_page.create_project(project_name)
    with allure.step("Дождаться завершения сетевого запроса по индикатору"):
        spinner_locator = (By.CSS_SELECTOR,
                           ".loading-spinner[data-type='save-project']")
        wait = WebDriverWait(browser, timeout=10)
        try:
            wait.until_not(
                EC.visibility_of_element_located(spinner_locator))
        except Exception as e:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="spinner_timeout",
                attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Индикатор сохранения висел дольше {timeout} секунд. "
                        f"Ошибка: {str(e)}")
    with allure.step(f"Проверить наличие проекта '{project_name}' в списке"):
        created_project_locator = (
            By.XPATH, f"//div[contains(text(), '{project_name}')]")
        try:
            wait.until(
                EC.visibility_of_element_located(created_project_locator))
        except TimeoutException:
            allure.attach(browser.get_screenshot_as_png(),
                          name="project_not_found",
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Проект '{project_name}' "
                        f"не отобразился в списке в течение 10 секунд "
                        f"после создания.")


@allure.epic("YouGile UI")
@allure.story("Добавление колонки")
@allure.title("Добавление колонки")
def test_add_column(browser, timeout=None):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
        comp_page.get_cart()
    with allure.step("Дождаться загрузки списка колонок"):
        wait = WebDriverWait(browser, timeout=15)
        wait.until(EC.presence_of_element_located(
            comp_page.COLUMN_CARD_LOCATOR))
    with allure.step("Получить список существующих колонок"):
        old_columns = comp_page.find_all_columns()
        old_count = len(old_columns)
        comp_page.open_company_page()
    with allure.step("Создать колонку"):
        comp_page.create_column()
    with allure.step("Дождаться завершения сетевого запроса по индикатору"):
        spinner_locator = (By.CSS_SELECTOR,
                           ".loading-spinner[data-type='save-column']")
        wait = WebDriverWait(browser, timeout=10)
        try:
            wait.until_not(EC.visibility_of_element_located(spinner_locator))
        except Exception as e:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="spinner_timeout",
                attachment_type=allure.attachment_type.PNG)
            pytest.fail(
                f"Индикатор сохранения висел дольше {timeout} секунд. "
                f"Ошибка: {str(e)}")
    with allure.step("Проверить увеличение количества колонок"):
        new_columns = comp_page.find_all_columns()
        new_count = len(new_columns)
    assert new_count == old_count + 1, (
        f"Ожидалось {old_count + 1} колонок, но найдено {new_count}."
        f"Колонка не была добавлена в DOM.")


@allure.epic("YouGile UI")
@allure.story("Добавление задачи")
@allure.title("Добавление задачи")
def test_add_task(browser, timeout=None):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
    with allure.step("Ввести наименование задачи"):
        task_name = 'Flyyyy'
    with allure.step("Добавить задачу"):
        comp_page.add_task(task_name)
    with allure.step(
            "Дождаться завершения сетевого запроса по индикатору"):
        spinner_locator = (
            By.CSS_SELECTOR, ".loading-spinner[data-type='save-task']")
        wait = WebDriverWait(browser, timeout=10)
        try:
            wait.until_not(EC.visibility_of_element_located(spinner_locator))
        except Exception as e:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="spinner_timeout",
                attachment_type=allure.attachment_type.PNG)
            pytest.fail(
                f"Индикатор сохранения висел дольше {timeout} секунд. "
                f"Ошибка: {str(e)}")
    with allure.step("Проверить наименование задачи"):
        locator = (By.XPATH, f"//span[contains(text(), '{task_name}')]")
        task_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located(locator)
        )
    actual_text = task_element.text
    assert actual_text.startswith(task_name), \
        (f"Задача не найдена или имя не совпадает. "
         f"Ожидалось начало '{task_name}', но получен '{actual_text}'")


@allure.epic("YouGile UI")
@allure.story("Удаление колонки")
@allure.title("Удаление колонки")
def test_del_column(browser):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
        comp_page.get_cart()
        with allure.step("Дождаться загрузки списка колонок"):
            wait = WebDriverWait(browser, timeout=15)
            wait.until(
                EC.presence_of_element_located(comp_page.COLUMN_CARD_LOCATOR))
        with allure.step("Получить список существующих колонок"):
            old_columns = comp_page.find_all_columns()
            old_count = len(old_columns)
            comp_page.open_company_page()
        with allure.step("Удалить колонку"):
            comp_page.del_column()
        with allure.step("Проверить увеличение количества колонок"):
            new_columns = comp_page.find_all_columns()
            new_count = len(new_columns)
        assert new_count == old_count - 1, (
            f"Ожидалось {old_count - 1} колонок, но найдено {new_count}."
            f"Колонка не была добавлена в DOM.")
