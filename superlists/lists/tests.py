from django.test import TestCase
from lists.models import Item

HOME_TEMPLATE = "home.html"


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_user_home_template(self):
        """Тест: использование корректного шаблона"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, HOME_TEMPLATE)

    def test_only_saves_items_when_necessary(self):
        """Тест: сохраняет элементы, только когда нужно"""
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        """Тест: можно сохранить post-запрос"""
        new_item_text = "A new list item"
        self.client.post("/", data={"item_text": new_item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_redirects_after_POST(self):
        """Тест: переадресация после post-запроса"""
        response = self.client.post("/", data={"item_text": "some text"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/lists/unique-list-in-world/")


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


class ListViewTest(TestCase):
    """Тест представления списка"""

    def test_uses_list_template(self):
        """Тест: используется шаблон списка"""
        response = self.client.get("/lists/unique-list-in-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        """Тест: отображаются все элементы списка"""
        new_item_texts = ("itemey 1", "itemey 2")
        [Item.objects.create(text=item_text) for item_text in new_item_texts]

        response = self.client.get("/lists/unique-list-in-world/")

        for item_text in new_item_texts:
            self.assertContains(response, item_text)
