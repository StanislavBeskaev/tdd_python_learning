from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.html import escape
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm
from lists.models import Item, List

HOME_TEMPLATE = "home.html"
User = get_user_model()


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

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        """Тест: владелец сохраняется, если пользователь аутентифицирован"""
        user = User.objects.create(email="a@b.com")
        self.client.force_login(user)
        self.client.post("/lists/new", data={"text": "new item"})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


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
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
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
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        """Тест: при недопустимом вводе на странице показывается ошибка"""
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        """Тест: ошибки валидации повторяющегося элемента оканчиваются на странице списков"""
        list_1 = List.objects.create()
        Item.objects.create(list=list_1, text="textey")

        response = self.client.post(f"/lists/{list_1.id}/", data={"text": "textey"})

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.count(), 1)


class MyListsTest(TestCase):
    """Тесты страницы 'Мои списки'"""

    def test_my_lists_url_renders_my_lists_template(self):
        """Используется корректный шаблон"""
        User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")

    def test_passes_correct_owner_to_template(self):
        """Тест: передаётся правильный владелец в шаблон"""
        User.objects.create(email="wrong@owner.com")
        correct_user = User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertEqual(response.context["owner"], correct_user)


class ShareListTest(TestCase):
    """Тесты представления для предоставления доступа к списку"""

    def test_post_redirects_to_lists_page(self):
        """Тест: POST запрос переадресуется на страницу списка"""
        user = User.objects.create(email="some@example.com")
        list_ = List.objects.create(owner=user)
        response = self.client.post(f"/lists/{list_.id}/share")
        self.assertRedirects(response, f"/lists/{list_.id}/")

    def test_email_added_to_shared(self):
        """Тест: email добавлен к поделившимся"""
        owner = User.objects.create(email="owner@example.com")
        other = User.objects.create(email="other@example.com")
        list_ = List.objects.create(owner=owner)

        self.client.post(f"/lists/{list_.id}/share", data={"sharee": other.email})
        self.assertIn(other, list_.shared_with.all())
