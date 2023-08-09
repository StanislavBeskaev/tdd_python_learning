from accounts.models import Token, User
from django.http import HttpRequest


class PasswordLessAuthenticationBackend:
    """Беспарольный backend для аутентификации"""

    def authenticate(self, request: HttpRequest, uid: str):
        """аутентифицировать"""
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email: str):
        """Получение пользователя"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
