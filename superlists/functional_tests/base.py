import os
import time
from typing import Callable

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

MAX_WAIT = 2
WAIT_TIMEOUT = 0.2


class FunctionalTest(StaticLiveServerTestCase):
    """Функциональный тест"""

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = f"http://{staging_server}"

    def tearDown(self) -> None:
        self.browser.quit()

    def add_new_element(self, text: str):
        """Добавить новый элемент в список"""
        inputbox = self.find_inputbox()
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

    def find_inputbox(self) -> WebElement:
        """Найти поле ввода элемента"""
        inputbox = self.browser.find_element(by=By.ID, value="id_text")
        return inputbox

    @staticmethod
    def wait_for(fn: Callable):
        """Ожидать"""
        start_time = time.monotonic()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.monotonic() - start_time > MAX_WAIT:
                    raise e
                time.sleep(WAIT_TIMEOUT)
