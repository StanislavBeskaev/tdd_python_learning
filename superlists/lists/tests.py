from django.test import TestCase

from lists.models import Item


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


class ItemModelTest(TestCase):
    """Тест модели элемента списка"""

    def test_saving_and_retrieving_item(self):
        """Тест сохранения и получения элементов списка"""
        first_item_text = "The first (ever) list item"
        second_item_text = "Item the second"

        first_item = Item()
        first_item.text = first_item_text
        first_item.save()

        second_item = Item()
        second_item.text = second_item_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(second_saved_item.text, second_item_text)
