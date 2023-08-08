from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты модели пользователя"""

    def test_user_is_valid_with_email_only(self):
        """Тест: пользователя можно создать только с email"""
        user = User(email='a@b.com')
        user.full_clean()
