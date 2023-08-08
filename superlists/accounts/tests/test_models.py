from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


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
