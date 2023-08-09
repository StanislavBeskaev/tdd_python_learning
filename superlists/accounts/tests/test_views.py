from unittest.mock import MagicMock, call, patch

from accounts.models import Token
from django.test import TestCase


class SendLoginEmailViewTest(TestCase):
    """Тесты представления, которое отправляет сообщение для входа в систему"""

    def send_login_email_request(self, email: str):
        return self.client.post("/accounts/send_login_email", data={"email": email})

    def test_redirect_to_home_page(self):
        """Тест: переадресуется на домашнюю страницу"""
        response = self.send_login_email_request("edith@example.com")
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail: MagicMock):
        """Тест: отправляется сообщение на адрес из метода post"""
        self.send_login_email_request("edith@example.com")
        self.assertTrue(mock_send_mail.called)
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(kwargs["subject"], "Your login link for Superlists")
        self.assertEqual(kwargs["from_email"], "noreply@superlists")
        self.assertEqual(kwargs["recipient_list"], ["edith@example.com"])

    def test_adds_success_message(self):
        """Тест: добавляется сообщение об успехе"""
        response = self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"}, follow=True)

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message, "Check your email, you'll find a message with a link that will log you into the site."
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        """Тест: создаётся маркер, связанный с электронной почтой"""
        self.send_login_email_request("edith@example.com")

        token = Token.objects.first()
        self.assertEqual(token.email, "edith@example.com")

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail: MagicMock):
        """Тест: отсылается ссылка на вход в систему, используя uid маркера"""
        self.send_login_email_request("edith@example.com")

        token = Token.objects.first()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        args, kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, kwargs["message"])


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    """Тесты представления входа в систему"""

    def test_redirects_to_home_page(self, mock_auth: MagicMock):
        """Тест: переадресуется на домашнюю страницу"""
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth: MagicMock):
        """Тест: вызывается authenticate с uid из GET-запроса"""
        uid = "abcd123"
        self.client.get(f"/accounts/login?token={uid}")
        self.assertEqual(mock_auth.authenticate.call_args, call(uid=uid))

    def test_calls_auth_with_user_if_there_is_one(self, mock_auth: MagicMock):
        """Тест: вызывает auth_login с пользователем, если такой имеется"""
        uid = "abcd123"
        response = self.client.get(f"/accounts/login?token={uid}")
        self.assertEqual(mock_auth.login.call_args, call(response.wsgi_request, mock_auth.authenticate.return_value))

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth: MagicMock):
        """Тест: не регистрируется в системе, если пользователь не аутентифицирован"""
        mock_auth.authenticate.return_value = None
        self.client.get(f"/accounts/login?token=abcd123")
        self.assertFalse(mock_auth.login.called)
