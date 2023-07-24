import unittest

from selenium import webdriver

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
        self.fail("Закончить тест!")

        # Ей сразу же предлагается ввести элемент списка

        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби - вязание рыболовных мушек)

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка

        # Текстовое поле по-прежнему приглашает её добавить ещё один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)

        # Страница снова обновляется, и теперь показывает оба элемента её списка

        # Эдит интересно, запомнит ли сайт её список. Далее она видит, что
        # сайт сгенерировал для неё уникальный URL-адрес - об этом
        # выводится небольшой текст с объяснениями.

        # Она посещает этот URL-адрес - её список по-прежнему там

        # Удовлетворённая, она снова ложится спать


if __name__ == '__main__':
    unittest.main(warnings="ignore")
