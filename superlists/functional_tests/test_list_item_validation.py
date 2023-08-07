from functional_tests.base import FunctionalTest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ItemValidationTest(FunctionalTest):
    """Тест валидации элемента списка"""

    def get_error_element(self) -> WebElement:
        """Получить элемент с ошибкой"""
        return self.browser.find_element(by=By.CSS_SELECTOR, value=".has-error")

    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        inputbox = self.find_inputbox()
        inputbox.send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value="#id_text:invalid"))

        # Эдит начинает набирать текст нового элемента и ошибка исчезает
        inputbox = self.find_inputbox()
        self.find_inputbox().send_keys("Buy milk")
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value="#id_text:valid"))

        # Она может отправить его успешно
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Как ни странно, Эдит решает отправить второй пустой элемент списка
        self.find_inputbox().send_keys(Keys.ENTER)

        # И снова браузер не подчинится
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value="#id_text:invalid"))

        # И она может исправиться, заполнив поле текстом
        inputbox = self.find_inputbox()
        inputbox.send_keys("Make tea")
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value="#id_text:valid"))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")

    def test_cannot_add_duplicate_items(self):
        """Тест: нельзя добавлять повторяющиеся элементы"""
        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.find_inputbox()
        inputbox.send_keys("Buy wellies")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy wellies")

        # Она случайно пытается ввести повторяющейся элемент
        inputbox = self.find_inputbox()
        inputbox.send_keys("Buy wellies")
        inputbox.send_keys(Keys.ENTER)

        # Она видит полезное сообщение об ошибке
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text,
                "You've already got this in your list",
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        """Тест: сообщения об ошибках очищаются при вводе"""
        # Эдит начинает список и вызывает ошибку валидации:
        self.browser.get(self.live_server_url)
        inputbox = self.find_inputbox()
        inputbox.send_keys("Banter too thick")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Banter too thick")

        inputbox = self.find_inputbox()
        inputbox.send_keys("Banter too thick")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))

        # Она начинает набирать в поле ввода, чтобы очистить ошибку
        inputbox = self.find_inputbox()
        inputbox.send_keys("a")

        # Она довольно от того, что сообщение об ошибке исчезает
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
