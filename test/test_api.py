import pytest
import allure
from YouGile.page.CompanyListPageApi import GetCompany
from YouGile.page.GetKeysPageApi import KeysPage
from YouGile.page.ProjectListApi import GetProjectList
from YouGile.page.ProjectsListApi import GetProjectsList
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
        get_list = comp_page.get_company_list()
    print(get_list)
    expected_count = get_list.get("paging", {}).get("count")
    with allure.step("Проверить что количество элементов в списке равно 0"):
        assert expected_count == 0


@allure.epic("YouGile Api")
@allure.story("Запрос листа компаний негативная проверка")
@allure.title("Запрос листа компаний без указания имени пользователя")
def test_get_company_list_negative():
    comp_page = GetCompany(auth_url)
    with pytest.raises(TypeError) as exc_info:
        comp_page.get_company_list(login, password)

    expected_error = ("GetCompany.get_company_list() "
                      "takes 1 positional argument but 3 were given")
    with allure.step("Проверить что сервер вернет ошибку "
                     "- должен быть один аргумент но дано 3"):
        assert str(exc_info.value) == expected_error


@allure.epic("YouGile Api")
@allure.story("Запрос списка ключей пользователя")
@allure.title("Запрос списка ключей пользователя")
def test_keys():
    keys_page = KeysPage(auth_url)
    with allure.step("Получить список ключей пользователя"):
        token_list = keys_page.get_keys()

    assert isinstance(token_list, list), \
        f"Ожидался список, получен {type(token_list)}"
    assert len(token_list) > 0, "Список ключей пуст"
    expected_key = os.getenv("API_TOKEN")

    with allure.step(f"Проверить наличие и значение ключа '{expected_key}'"):
        actual_key = token_list[0].get('key')
    assert actual_key == expected_key, (f"Ожидался ключ {expected_key},"
                                        f"" f"получен: {actual_key}")


@allure.epic("YouGile Api")
@allure.story("Получение списка проектов компании")
@allure.title("Получение списка проектов компании")
def test_get_projects():
    all_projects = GetProjectsList(auth_url)
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
    all_projects = GetProjectsList(auth_url)
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
@allure.story("Создание проекта негативная проверка")
@allure.title("Создание проекта без токена авторизации")
def test_create_project_negative():
    create_pro = CreateProject(auth_url)
    with allure.step("Создать новый проект без заголовка с токеном"):
        result = create_pro.post_project_negative()

    with allure.step("Проверить что ответ сервера с статус кодом 401 "
                     "- Unauthorized"):
        assert result["statusCode"] == 401, \
            f"Ожидался код 401, получен {result.get('statusCode')}"
        assert "error" in result
        assert result["error"] == "Unauthorized"
        assert "message" in result
        assert result["message"] == "Unauthorized"


@allure.epic("YouGile Api")
@allure.story("Изменение наименования проекта")
@allure.title("Изменение наименования проекта")
def test_change_pro():
    expected_title = "River-Volga"
    changer = ChangeProject(auth_url)
    getter = GetProjectList(auth_url)
    with allure.step(f"Отправить запрос на изменение названия на "
                     f"'{expected_title}'"):
        update_result = changer.project_list(project_id)
        assert 'id' in update_result, (f"Сервер не вернул id."
                                       f"Ответ: {update_result}")

    with allure.step(
            "Получить проект заново через GET и проверить поле title"):
        current_data = getter.project_list(project_id)
        actual_title = current_data.get('title')

    with (allure.step(
            "Проверить через assert, что название изменилось в базе данных")):
        assert actual_title == expected_title, (
            f"Провал теста: название в базе"
            f"не совпадает с ожидаемой строкой.\n"
            f"Ожидалось: '{expected_title}'\n"
            f"Фактически пришло в GET: '{actual_title}'\n"
            f"Полный ответ GET: {current_data}\n"
            f"(Ответ сервера на PUT был: {update_result})")


@allure.epic("YouGile Api")
@allure.story("Изменение наименования проекта негативная проверка")
@allure.title("Изменения наименования проекта без добавления id")
def test_negative_change_pro():
    to_change = ChangeProject(auth_url)
    with pytest.raises(TypeError) as exc_info:
        to_change.project_list()
        with allure.step("Проверить что сервер вернет ответ с ошибкой "
                         "так как аргумент project_id не передан"):
            assert ("missing 1 required positional argument: 'project_id'"
                    in str(exc_info.value))
