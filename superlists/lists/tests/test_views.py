from django.test import TestCase
from django.utils.html import escape
from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List

HOME_TEMPLATE = "home.html"


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_user_home_template(self):
        """Тест: использование корректного шаблона"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, HOME_TEMPLATE)

    def test_home_page_uses_item_form(self):
        """Тест: домашняя страница использует форму для элемента"""
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)


class NewListTest(TestCase):
    """Тест нового списка"""

    def test_can_save_a_POST_request(self):
        """Тест: можно сохранить post-запрос"""
        new_item_text = "A new list item"
        self.client.post("/lists/new", data={"text": new_item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_redirects_after_POST(self):
        """Тест: переадресация после post-запроса"""
        response = self.client.post("/lists/new", data={"text": "some text"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_for_invalid_input_renders_home_template(self):
        """Тест: на недопустимый ввод: отображается шаблон home"""
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_shown_on_home_page(self):
        """Тест: ошибки валидации выводятся на домашней странице"""
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        """Тест: на недопустимый ввод, форма передаётся в шаблон"""
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        """Тест: не сохраняются недопустимые элементы списка"""
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    """Тест представления списка"""

    def post_invalid_input(self):
        """Отправка недопустимого ввода"""
        list_ = List.objects.create()
        return self.client.post(f"/lists/{list_.id}/", data={"text": ""})

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

        self.client.post(f"/lists/{correct_list.id}/", data={"text": "A new item for an existing list"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """Тест: post-запрос переадресуется в представление списка"""
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/", data={"text": "A new item for an existing list"})

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_invalid_list_items_arent_saved(self):
        """Тест: не сохраняются недопустимые элементы списка"""
        list_ = List.objects.create()
        self.client.post(f"/lists/{list_.id}/", data={"text": ""})
        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 0)

    def test_display_item_form(self):
        """Тест: отображения формы для элемента"""
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertIsInstance(response.context["form"], ItemForm)
        self.assertContains(response, 'name="text')

    def test_for_invalid_input_nothing_saved_to_db(self):
        """Тест: при недопустимом вводе ничего не сохраняется в базу"""
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        """Тест: при недопустимом вводе отображается шаблон списка"""
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        """Тест: при недопустимом вводе форма передаётся в шаблон"""
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        """Тест: при недопустимом вводе на странице показывается ошибка"""
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
