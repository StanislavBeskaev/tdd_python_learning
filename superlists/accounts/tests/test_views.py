import accounts.views
from django.test import TestCase

from accounts import views


class SendLoginEmailViewTest(TestCase):
    """Тесты представления, которое отправляет сообщение для входа в систему"""

    def test_redirect_to_home_page(self):
        """Тест: переадресуется на домашнюю страницу"""
        response = self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        self.assertRedirects(response, "/")

    def test_sends_mail_to_address_from_post(self):
        """Тест: отправляется сообщение на адрес из метода post"""
        self.send_mail_called = False

        def fake_send_mail(subject, message, from_email, recipient_list):
            """Поддельная функция send_mail"""
            self.send_mail_called = True
            self.subject = subject
            self.message = message
            self.from_email = from_email
            self.to_list = recipient_list

        accounts.views.send_mail = fake_send_mail

        response = self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, "Your login link for Superlists")
        self.assertEqual(self.from_email, "noreply@superlists")
        self.assertEqual(self.to_list, ["edith@example.com"])
