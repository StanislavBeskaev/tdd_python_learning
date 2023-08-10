import os
import time
from typing import Callable

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from functional_tests.server_tools import reset_database
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

MAX_WAIT = 2
WAIT_TIMEOUT = 0.2


def wait(fn: Callable) -> Callable:
    def modified_fn(*args, **kwargs):
        start_time = time.monotonic()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.monotonic() - start_time > MAX_WAIT:
                    raise e
                time.sleep(WAIT_TIMEOUT)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """Функциональный тест"""

    def setUp(self) -> None:
        self.init_browser()
        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            self.live_server_url = f"http://{self.staging_server}"
            reset_database(self.staging_server)

    def init_browser(self):
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def add_new_element(self, text: str):
        """Добавить новый элемент в список"""
        inputbox = self.find_inputbox()
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    @wait
    def wait_for_row_in_list_table(self, row_text: str):
        """Ожидать строку в таблице списка"""
        table = self.browser.find_element(by=By.ID, value="id_list_table")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")
        self.assertIn(row_text, [row.text for row in rows])

    def find_inputbox(self) -> WebElement:
        """Найти поле ввода элемента"""
        inputbox = self.browser.find_element(by=By.ID, value="id_text")
        return inputbox

    @wait
    def wait_for(self, fn: Callable):
        """Ожидать"""
        return fn()

    @wait
    def wait_to_be_logged_in(self, email: str):
        """Ожидать входа в систему"""
        self.browser.find_element(by=By.LINK_TEXT, value="Log out")
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value=".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email: str):
        """Ожидать выхода из системы"""
        self.browser.find_element(by=By.NAME, value="email")
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value=".navbar")
        self.assertNotIn(email, navbar.text)
