import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

MAX_WAIT = 2
WAIT_TIMEOUT = 0.2


class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_for_one_user(self):
        """Тест: можно начать список для одного пользователя"""
        # Эдит слышала про новое крутое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value="h1").text
        self.assertIn("To-Do", header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби - вязание рыболовных мушек)
        inputbox.send_keys("Купить павлиньи перья")

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Купить павлиньи перья")

        # Текстовое поле по-прежнему приглашает её добавить ещё один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)
        self.add_new_element("Сделать мушку из павлиньих перьев")

        # Страница снова обновляется, и теперь показывает оба элемента её списка
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")
        self.wait_for_row_in_list_table("2: Сделать мушку из павлиньих перьев")

        # Удовлетворённая, она снова ложится спать

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        self.add_new_element("Купить павлиньи перья")
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")

        # Она замечает, что её список имеет уникальный URL-адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Теперь новый пользователь, Фрэнсис, приходит на сайт

        # Используем новый сеанс браузера, тем самым обеспечивая, что бы никакая
        # информация от Эдит не прошла через cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Фрэнсис посещают домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by=By.TAG_NAME, value="body").text
        self.assertNotIn("Купить павлиньи перья", page_text)
        self.assertNotIn("Сделать мушку", page_text)

        # Фрэнсис начинает новый список, вводя новый элемент. Он менее интересен, чем список Эдит
        self.add_new_element("Купить молоко")

        self.wait_for_row_in_list_table("1: Купить молоко")

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element(by=By.TAG_NAME, value="body").text
        self.assertNotIn("Купить павлиньи перья", page_text)
        self.assertIn("Купить молоко", page_text)

        # Удовлетворённые, они оба ложатся спать

    def add_new_element(self, text: str):
        """Добавить новый элемент в список"""
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def wait_for_row_in_list_table(self, row_text: str):
        """Ожидать строку в таблице списка"""
        start_time = time.monotonic()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value="id_list_table")
                rows = table.find_elements(by=By.TAG_NAME, value="tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.monotonic() - start_time > MAX_WAIT:
                    raise e
                time.sleep(WAIT_TIMEOUT)
