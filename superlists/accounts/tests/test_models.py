from django.test import TestCase
from django.contrib import auth

from accounts.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):
    """Тесты модели пользователя"""

    def test_user_is_valid_with_email_only(self):
        """Тест: пользователя можно создать только с email"""
        user = User(email='a@b.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        """Тест: адрес электронной почты является первичным ключом"""
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_no_problem_with_auth_login(self):
        """Тест: проблем с auth_login нет"""
        user = User.objects.create(email="edith@example.com")
        user.backend = ""
        request = self.client.request().wsgi_request
        auth.login(request, user)  # не должно поднять исключение


class TokenModelTest(TestCase):
    """Тесты модели маркера"""

    def test_links_user_with_auto_generated_uid(self):
        """Тест: соединяет пользователя с автогенерированным uid"""
        token_1 = Token.objects.create(email='a@b.com')
        token_2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token_1.uid, token_2.uid)
