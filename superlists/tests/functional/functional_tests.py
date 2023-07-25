import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

APP_URL = "http://localhost:8000"


class NewVisitorTest(unittest.TestCase):
    """Тест нового посетителя"""

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Можно начать список и получить его позже"""
        # Эдит слышала про новое крутое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get(APP_URL)

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
        time.sleep(1)  # Явное ожидание перезагрузки страницы

        table = self.browser.find_element(by=By.ID, value="id_list_table")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")
        self.assertIn("1: Купить павлиньи перья", [row.text for row in rows])

        # Текстовое поле по-прежнему приглашает её добавить ещё один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        inputbox.send_keys("Сделать мушку из павлиньих перьев")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница снова обновляется, и теперь показывает оба элемента её списка
        table = self.browser.find_element(by=By.ID, value="id_list_table")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")
        self.assertIn("1: Купить павлиньи перья", [row.text for row in rows])
        self.assertIn("2: Сделать мушку из павлиньих перьев", [row.text for row in rows])

        # Эдит интересно, запомнит ли сайт её список. Далее она видит, что
        # сайт сгенерировал для неё уникальный URL-адрес - об этом
        # выводится небольшой текст с объяснениями.
        self.fail("Закончить тест!")

        # Она посещает этот URL-адрес - её список по-прежнему там

        # Удовлетворённая, она снова ложится спать


if __name__ == '__main__':
    unittest.main(warnings="ignore")
