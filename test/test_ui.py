import pytest
import uuid
import allure
from YouGile.page.AuthPageUI import AuthPage
from YouGile.page.CompanyPageUI import CompanyPage
import os
from dotenv import load_dotenv
from time import sleep

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
    sleep(5)


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
    assert actual_url == 'https://ru.yougile.com/team/projects#ID-49', \
        f"Тест НЕ пройден. Ожидался полный URL {actual_url}, но получен другой"


@allure.epic("YouGile UI")
@allure.story("Создание проекта")
@allure.title("Создание проекта")
def test_create_project(browser):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    sleep(5)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
    sleep(5)
    with allure.step("Ввести название проекта"):
        project_name = f"Skyeng_{uuid.uuid4().hex[:6]}"
    create_page = CompanyPage(browser)
    with allure.step("Создать проект"):
        create_page.create_project(project_name)
    sleep(5)


@allure.epic("YouGile UI")
@allure.story("Добавление колонки")
@allure.title("Добавление колонки")
def test_add_column(browser):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    sleep(5)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
    sleep(5)
    with allure.step("Создать колонку"):
        comp_page.create_column()
    sleep(5)


@allure.epic("YouGile UI")
@allure.story("Добавление задачи")
@allure.title("Добавление задачи")
def test_add_task(browser):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    sleep(5)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
    sleep(5)
    with allure.step("Ввести наименование задачи"):
        task_name = 'Flyyyy'
    with allure.step("Добавить задачу"):
        comp_page.add_task(task_name)
    sleep(5)


@allure.epic("YouGile UI")
@allure.story("Удаление колонки")
@allure.title("Удаление колонки")
def test_del_column(browser):
    auth_page = AuthPage(browser)
    with allure.step("Перейти на страницу авторизации"):
        auth_page.go()
    with allure.step("Ввести email и password"):
        auth_page.login_as(email, password)
    sleep(5)
    comp_page = CompanyPage(browser)
    with allure.step("Открыть страницу проектов"):
        comp_page.open_company_page()
    sleep(5)
    with allure.step("Удалить колонку"):
        comp_page.del_column()
    sleep(10)
