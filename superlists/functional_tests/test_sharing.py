from selenium import webdriver
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage
from functional_tests.my_list_page import MyListPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    """Тест обмена данными"""

    def test_can_share_a_list_with_another_user(self):
        """Тест: можно обмениваться списком с ещё одним пользователем"""
        # Эдит является зарегистрированным пользователем
        self.create_pre_authentication_session(email="edith@example.com")
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Её друг Анцифер тоже зависает на сайте списков
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authentication_session(email="oniciferous@example.com")

        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item("Get help")

        # Она замечает опцию "Поделится этим списком"
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute("placeholder"), "your-friend@example.com")

        # Она делится своим списком.
        # Страница обновляется и сообщает, что теперь страница используется совместно с Анцифером
        list_page.share_list_with("oniciferous@example.com")

        # Анцифер переходит на страницу списков в своем браузере
        self.browser = oni_browser
        MyListPage(self).go_to_my_lists_page()

        # Он видит на ней список Эдит!
        self.browser.find_element(by=By.LINK_TEXT, value="Get help").click()

        # На странице, которую Анцифер видит, говорится, что это список Эдит
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(), "edith@example.com"
        ))

        # Он добавляет элемент в список
        list_page.add_list_item("Hi Edith")

        # Когда Эдит обновляет страницу, она видит дополнение Анцифера
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table("Hi Edith", 2)


