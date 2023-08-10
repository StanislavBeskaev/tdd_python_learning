from django.conf import settings
from django.contrib.auth import get_user_model
from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_pre_authentication_session
from functional_tests.server_tools import create_session_on_server

User = get_user_model()


class MyListTest(FunctionalTest):
    """Тест приложения 'Мои списки'"""

    def create_pre_authentication_session(self, email: str) -> None:
        """Создать предварительно аутентифицированный сеанс"""
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authentication_session(email=email)

        # Установить cookie, которые нужны для первого посещения домена.
        # Страницы 404 загружаются быстрее всего
        self.browser.get(self.live_server_url + "/404_no_such_url")
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/"))

    def test_logged_in_lists_are_saved_as_my_lists(self):
        """Тест: списки зарегистрированных пользователей сохраняются как 'мои списки'"""
        email = "edith@example.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email=email)

        # Эдит является зарегистрированным пользователем
        self.create_pre_authentication_session(email=email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email=email)
