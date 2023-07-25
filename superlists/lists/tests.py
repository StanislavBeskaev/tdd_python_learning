from django.test import TestCase


HOME_TEMPLATE = "home.html"


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_user_home_template(self):
        """Тест: использование корректного шаблона"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, HOME_TEMPLATE)

    def test_can_save_a_POST_request(self):
        """Тест: можно сохранить post-запрос"""
        new_item = "A new list item"
        response = self.client.post("/", data={"item_text": new_item})
        self.assertIn(new_item, response.content.decode())
        self.assertTemplateUsed(response, HOME_TEMPLATE)
