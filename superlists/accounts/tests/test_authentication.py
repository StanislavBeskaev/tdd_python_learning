from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.authentication import PasswordLessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticationTest(TestCase):
    """Тесты аутентификации"""

    def test_returns_None_if_no_such_token(self):
        """Тест: возвращается None, если нет такого маркера"""
        result = PasswordLessAuthenticationBackend().authenticate(HttpRequest(), 'no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """Тест: возвращается новый пользователь с правильной электронной почтой, если маркер существует"""
        email = "edith@example.com"
        token = Token.objects.create(email=email)
        user = PasswordLessAuthenticationBackend().authenticate(HttpRequest(), token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """Тест: возвращается существующий пользователь с правильной электронной почтой, если маркер существует"""
        email = "edith@example.com"
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordLessAuthenticationBackend().authenticate(HttpRequest(),token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    """Тесты получения пользователя"""

    def test_gets_user_by_email(self):
        """Тест: получение пользователя по адресу электронной почты"""
        User.objects.create(email="another@example.com")
        desired_user = User.objects.create(email="edith@example.com")

        found_user = PasswordLessAuthenticationBackend().get_user("edith@example.com")
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        """Тест: возвращается None, если нет пользователя с таким адресом электронной почты"""
        self.assertIsNone(PasswordLessAuthenticationBackend().get_user("edith@example.com"))
