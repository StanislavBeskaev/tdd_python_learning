from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from superlists.lists.views import home_page


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_root_url_resolve_to_home_page_view(self):
        """Тест: корневой url преобразуется в представление домашней страницы"""
        found = resolve("/")
        self.assertEquals(found.func, home_page)

    def test_home_page_return_correct_html(self):
        """Тест: домашняя страница возвращает корректный html"""
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>"))
