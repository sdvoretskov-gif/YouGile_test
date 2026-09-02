import re
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CompanyPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

    def open_company_page(self):
        (WebDriverWait(self.__driver, 15).
         until(EC.visibility_of_element_located(
             (By.XPATH, "//div[contains(text(),'Моя компания')]"))))
        self.__driver.find_element(
            By.XPATH, "//div[contains(text(),'Моя компания')]").click()

    def current_url(self) -> str:
        return self.__driver.current_url

    def company_name(self):
        locator = (By.XPATH, "//span[normalize-space()="
                             "'https://potok-1302.yougile.com']")

        company_element = WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located(locator)
        )

        actual_text = company_element.text
        expected_text = "https://potok-1302.yougile.com"

        assert actual_text == expected_text, \
            f"Ожидался текст '{expected_text}', но получен '{actual_text}'"

        return actual_text

    def create_project(self, project_name: str):
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located(
             (By.XPATH,
              "//span[normalize-space()='https://potok-1302.yougile.com']"))))

        add_card = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-testid='add-project-card']")))
        add_card.click()

        template_button = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'Проект с задачами')]")))
        template_button.click()

        input_field = WebDriverWait(self.__driver, 15).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder="
                                  "'Введите название проекта…']")))
        input_field.clear()
        input_field.send_keys(project_name)

        submit_button = (WebDriverWait(self.__driver, 15).
                         until(EC.element_to_be_clickable(
                            (By.XPATH, "//div[contains(text(), "
                                       "'Добавить проект с задачами')]"))))
        submit_button.click()

        actual_title_element = WebDriverWait(self.__driver, 15).until(
            EC.visibility_of_element_located(
             (By.XPATH, "//div[@class='flex-none "
                        "text-sm-semibold text-panel-text-primary']")))

        actual_title_text = actual_title_element.text.strip()
        expected_title = f"Проект {project_name}"

        normalized_title = (
            actual_title_text
            .replace('“', '"')
            .replace('”', '"'))

        normalized_title = normalized_title.replace('"', '')

        final_title = re.sub(r'\s+', ' ', normalized_title).strip()

        assert final_title == expected_title, \
            (f"\nТест НЕ пройден!\n" f"Ожидалось название"
             f"'{expected_title}'\n" f"Фактическое название:"
             f"'{final_title}'")

    def create_column(self):
        click_card = self.__driver.find_element(
            By.XPATH, "//div[@data-testid='project-title' "
                      "and text()='Skyeng']")
        click_card.click()

        add_column = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Создать колонку')]")))
        add_column.click()
        (self.__driver.switch_to.active_element.
         send_keys("Новая колонка", Keys.RETURN))

    def add_task(self, task_name: str):
        click_card = self.__driver.find_element(
            By.XPATH, "//div[@data-testid='project-title' "
                      "and text()='Skyeng']")
        click_card.click()

        add_column = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Создать колонку')]")))
        add_column.click()
        self.__driver.switch_to.active_element.send_keys(
            "Новая колонка", Keys.RETURN)

        click_field = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Добавить задачу')]")))
        click_field.click()

        inter_name = WebDriverWait(self.__driver, 15).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'textarea[placeholder^='
                                  '"Введите название задачи…"]')))
        inter_name.send_keys(task_name)
        inter_name.send_keys(Keys.ENTER)

    def del_column(self):
        click_card = self.__driver.find_element(
            By.XPATH, "//div[@data-testid='project-title' "
                      "and text()='Skyeng']")
        click_card.click()

        click_col = self.__driver.find_element(
            By.XPATH, "//div[@class='hint__cnt relative w-24 h-24 "
                      "cursor-pointer text-secondary hover:text-action-hover "
                      "active:text-action-pressed flex-none -mx-4 select-none "
                      "flex items-center justify-center group/icon-button']//"
                      "*[name()='svg']")
        click_col.click()

        click_button = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'Удалить')]")))
        click_button.click()

        click_one_more_time = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='text-left "
                           "flex items-center justify-center w-full']"
                           "[contains(text(),'Удалить')]")))
        click_one_more_time.click()
