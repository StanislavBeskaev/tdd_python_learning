from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from functional_tests.base import wait, FunctionalTest


class ListPage:
    """Страница списка"""

    def __init__(self, test: FunctionalTest):
        self.test = test

    def get_table_rows(self) -> list[WebElement]:
        """Получить строки таблицы"""
        return self.test.browser.find_elements(by=By.CSS_SELECTOR, value="#id_list_table rt")

    @wait
    def wait_for_row_in_list_table(self, item_text: str, item_number: int) -> None:
        """Ожидать строку в таблице списка"""
        row_text = f"{item_number}: {item_text}"
        rows = self.get_table_rows()
        self.test.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self) -> WebElement:
        """Получить поле ввода элемента"""
        return self.test.browser.find_element(by=By.ID, value="id_text")

    def add_list_item(self, item_text: str) -> "ListPage":
        """Добавить элемент в список"""
        new_item_number = len(self.get_table_rows()) + 1
        input_box = self.get_item_input_box()
        input_box.send_keys(item_text)
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text, new_item_number)
        return self

    def get_share_box(self) -> WebElement:
        """Получить поле для обмена списками"""
        return self.test.browser.find_element(by=By.CSS_SELECTOR, value='input[name="sharee"]')

    def get_shared_with_list(self) -> list[WebElement]:
        """Получить список от того, кто им делится"""
        return self.test.browser.find_elements(by=By.CSS_SELECTOR, value=".list-sharee")

    def share_list_with(self, email: str) -> None:
        """Поделится списком с"""
        share_box = self.get_share_box()
        share_box.send_keys(email)
        share_box.send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(email, [item.text for item in self.get_shared_with_list()]))
