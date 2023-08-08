from accounts.models import User, Token


class PasswordLessAuthenticationBackend:
    """Беспарольный backend для аутентификации"""

    def authenticate(self, uid):
        """аутентифицировать"""
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None
