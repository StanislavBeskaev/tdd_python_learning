from functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By


class MyListPage:
    """Моя страница списков"""

    def __init__(self, test: FunctionalTest):
        self.test = test

    def go_to_my_lists_page(self):
        """Перейти на мою страницу списков"""
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element(by=By.LINK_TEXT, value="My lists").click()
        self.test.wait_for(
            lambda: self.test.assertEqual(self.test.browser.find_element(by=By.TAG_NAME, value="h1").text, "My lists")
        )
        return self
