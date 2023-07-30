from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List

HOME_TEMPLATE = "home.html"


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_user_home_template(self):
        """Тест: использование корректного шаблона"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, HOME_TEMPLATE)


class NewListTest(TestCase):
    """Тест нового списка"""

    def test_can_save_a_POST_request(self):
        """Тест: можно сохранить post-запрос"""
        new_item_text = "A new list item"
        self.client.post("/lists/new", data={"item_text": new_item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_redirects_after_POST(self):
        """Тест: переадресация после post-запроса"""
        response = self.client.post("/lists/new", data={"item_text": "some text"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """Тест: ошибки валидации отсылаются назад в шаблон домашней страницы"""
        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        """Тест: не сохраняются недопустимые элементы списка"""
        self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    """Тест представления списка"""

    def test_uses_list_template(self):
        """Тест: используется шаблон списка"""
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        """Тест: отображаются элементы только для этого списка'"""
        correct_list = List.objects.create()
        new_item_texts = ("itemey 1", "itemey 2")
        [Item.objects.create(text=item_text, list=correct_list) for item_text in new_item_texts]

        other_list = List.objects.create()
        other_list_item_texts = ("другой элемент 1 списка", "другой элемент 2 списка")
        [Item.objects.create(text=item_text, list=other_list) for item_text in other_list_item_texts]

        response = self.client.get(f"/lists/{correct_list.id}/")

        for item_text in new_item_texts:
            self.assertContains(response, item_text)

        for item_text in other_list_item_texts:
            self.assertNotContains(response, item_text)

    def test_passed_correct_list_to_template(self):
        """Тест: в шаблон передаётся правильный список"""
        _ = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Тест: можно сохранить post-запрос в существующий список"""
        _ = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/", data={"item_text": "A new item for an existing list"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """Тест: post-запрос переадресуется в представление списка"""
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/", data={"item_text": "A new item for an existing list"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
