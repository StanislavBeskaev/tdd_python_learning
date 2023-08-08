from unittest.mock import patch, MagicMock

from django.test import TestCase


class SendLoginEmailViewTest(TestCase):
    """Тесты представления, которое отправляет сообщение для входа в систему"""

    def test_redirect_to_home_page(self):
        """Тест: переадресуется на домашнюю страницу"""
        response = self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail: MagicMock):
        """Тест: отправляется сообщение на адрес из метода post"""
        self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})

        self.assertTrue(mock_send_mail.called)
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(kwargs["subject"], "Your login link for Superlists")
        self.assertEqual(kwargs["message"], "body text tbc")
        self.assertEqual(kwargs["from_email"], "noreply@superlists")
        self.assertEqual(kwargs["recipient_list"], ["edith@example.com"])
