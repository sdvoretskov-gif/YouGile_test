import pytest
import allure
from YouGile.page.CompanyListPageApi import GetCompany
from YouGile.page.AuthPageApi import AuthPage
from YouGile.page.GetKeysPageApi import KeysPage
from YouGile.page.ProjectListApi import GetProjectList
from YouGile.page.ChangeProPageApi import ChangeProject
from YouGile.page.CreateProApi import CreateProject
import os
from dotenv import load_dotenv

load_dotenv()

pytestmark = [pytest.mark.api]

auth_url = "https://ru.yougile.com/api-v2/"
login = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
name = "Сергей Д"
project_id = os.getenv("PROJECTID")


@allure.epic("YouGile Api")
@allure.story("Запрос листа компаний")
@allure.title("Запрос листа компаний")
def test_get_company_list():
    comp_page = GetCompany(auth_url)
    with allure.step("Получить лист компаний"):
        get_list = comp_page.get_company_list(login, password, name)
    print(get_list)


@allure.epic("YouGile Api")
@allure.story("Запрос листа компаний негативная проверка")
@allure.title("Запрос листа компаний негативная проверка")
def test_get_company_list_negative():
    comp_page = GetCompany(auth_url)
    with allure.step("Получить лист компаний"):
        get_list = comp_page.get_company_list(login, password)

    status_code = get_list.get('statusCode')
    with allure.step("Проверить получение ожидаемого статус кода"):
        assert (status_code == 400
                ), (f"Ожидался статус 400 Bad Request Error, "
                    f"получен: {status_code}")

    error_msg = get_list.get('message', '').lower()
    assert 'not found' in error_msg or 'cannot' in error_msg


@allure.epic("YouGile Api")
@allure.story("Запрос на получение Api Key")
@allure.title("Запрос на получение Api Key")
def test_auth():
    auth_page = AuthPage(auth_url)
    with allure.step("Получить Api Key"):
        token_key = auth_page.get_token()
    print(token_key)


@allure.epic("YouGile Api")
@allure.story("Запрос списка ключей пользователя")
@allure.title("Запрос списка ключей пользователя")
def test_keys():
    keys_page = KeysPage(auth_url)
    with allure.step("Получить список ключей пользователя"):
        token_list = keys_page.get_keys()
    print(token_list)


@allure.epic("YouGile Api")
@allure.story("Получение списка проектов компании")
@allure.title("Получение списка проектов компании")
def test_get_projects():
    all_projects = GetProjectList(auth_url)
    with allure.step(
            "Получить сведения о пагинации и список проектов компаний"):
        result = all_projects.project_list()
    with allure.step("Передать в переменную список проектов компании"):
        content = result["content"]
    with allure.step(
            "Вывести в терминал сведения о пагинации "
            "и список проектов компании"):
        print(result)
    with allure.step("Вывести в терминал список проектов"):
        print(content)
    with allure.step("Передать в переменную длину списка проектов"):
        projects_count = len(content)
    with allure.step("Вывести в терминал количество проектов в списке"):
        print(f"\nКоличество проектов в списке: {projects_count}")
    with allure.step("Убедится что количество проектов в пагинации "
                     "соответствует количеству проектов компании из списка"):
        expected_count = result.get("paging", {}).get("count")
    assert projects_count == expected_count, (
        f"Количество элементов в 'content' "
        f"({projects_count}) " f"не совпадает со счетчиком в 'paging' "
        f"({expected_count})")


@allure.epic("YouGile Api")
@allure.story("Создание проекта")
@allure.title("Создание проекта")
def test_create_project():
    all_projects = GetProjectList(auth_url)
    with allure.step("Получить список проектов до"):
        result_before = all_projects.project_list()
    with allure.step("Передать в переменную длину списка проектов до"):
        len_before = len(result_before["content"])
    create_pro = CreateProject(auth_url)
    with allure.step("Создать новый проект"):
        result = create_pro.post_project()
    with allure.step("Вывести в консоль id созданного проекта"):
        print(result)
    with allure.step("Получить список проектов после"):
        result_after = all_projects.project_list()
    with allure.step("Передать в переменную длину списка проектов после"):
        len_after = len(result_after["content"])
    with allure.step("Проверить что длинна списка проектов увеличилась на 1"):
        assert len_after - len_before == 1


@allure.epic("YouGile Api")
@allure.story("Изменение наименования проекта")
@allure.title("Изменение наименования проекта")
def test_change_pro():
    to_change = ChangeProject(auth_url)
    with allure.step("Найти проект по его id и изменить название проекта"):
        result = to_change.project_list(project_id)
    with allure.step("Вывести в консоль новый id проекта"):
        print(result)


@allure.epic("YouGile Api")
@allure.story("Изменение наименования проекта негативная проверка")
@allure.title("Изменения наименования проекта негативная проверка")
def test_negative_change_pro():
    to_change = ChangeProject(auth_url)
    with allure.step("Направить запрос на изменение проекта без указания id"):
        result = to_change.project_list()
    with allure.step("Вывести в консоль результат запроса"):
        print(result)
