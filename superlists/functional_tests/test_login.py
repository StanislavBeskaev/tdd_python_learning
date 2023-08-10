import os
import poplib
import re
import time

from django.core import mail
from functional_tests.base import FunctionalTest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

SUBJECT = "Your login link for Superlists"
MAX_WAIT_EMAIL_SECONDS = 60
EMAIL_WAIT_TIMEOUT = 2


class LoginTest(FunctionalTest):
    """Тест регистрации в системе"""

    def wait_for_email(self, test_email: str, subject: str) -> str:
        """Ожидать электронное сообщение"""
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.monotonic()
        inbox = poplib.POP3_SSL("pop.gmail.com")
        try:
            inbox.user(test_email)
            print(f"start reading mail for {test_email}")
            inbox.pass_(os.environ.get("EMAIL_PASSWORD"))
            while time.monotonic() - start < MAX_WAIT_EMAIL_SECONDS:
                # Получить 10 самых новых сообщений
                count, _ = inbox.stat()
                for message_index in reversed(range(max(1, count - 10), count + 1)):
                    print(f"getting msg {message_index}")
                    _, lines, __ = inbox.retr(message_index)
                    lines = [line.decode("utf-8") for line in lines]
                    if f"Subject: {subject}" in lines:
                        email_id = message_index
                        email_body = "\n".join(lines)
                        return email_body
                time.sleep(EMAIL_WAIT_TIMEOUT)
        finally:
            if email_id:
                inbox.dele(email_id)
                print(f"delete message {email_id}")
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        """Тест: можно получить ссылку по почте для регистрации"""
        # Эдит заходит на офигительный сайт для суперсписков и впервые замечает раздел "войти" в навигационной панели
        # Он говорит ей ввести свой адрес электронной почты, что она и делает
        if self.staging_server:
            test_email = os.environ.get("EMAIL_USER")
        else:
            test_email = "edith@example_com"
        self.browser.get(self.live_server_url)
        email_input = self.browser.find_element(by=By.NAME, value="email")
        email_input.send_keys(test_email)
        email_input.send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ей на почту было выслано электронное письмо
        self.wait_for(
            lambda: self.assertIn("Check your email", self.browser.find_element(by=By.TAG_NAME, value="body").text)
        )

        # Эдит проверяет свою почту и находит сообщение
        email_body = self.wait_for_email(test_email=test_email, subject=SUBJECT)

        # Оно содержит ссылку на url-адрес
        self.assertIn("Use this link to log in", email_body)
        url_search = re.search(r"http://.+/.+$", email_body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email_body}")

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Эдит нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе
        self.wait_to_be_logged_in(email=test_email)

        # Теперь она выходит из системы
        self.browser.find_element(by=By.LINK_TEXT, value="Log out").click()

        # Она вышла из системы
        self.wait_to_be_logged_out(email=test_email)
