from django.test import TestCase
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


class NewItemTest(TestCase):
    """Тест нового элемента списка"""

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Тест: можно сохранить post-запрос в существующий список"""
        _ = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add_item", data={"item_text": "A new item for an existing list"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """Тест: переадресуется в представление списка"""
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item", data={"item_text": "A new item for an existing list"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")


class ListAndItemModelsTest(TestCase):
    """Тест модели элемента списка"""

    def test_saving_and_retrieving_item(self):
        """Тест сохранения и получения элементов списка"""
        list_ = List()
        list_.save()

        first_item_text = "The first (ever) list item"
        second_item_text = "Item the second"

        first_item = Item()
        first_item.text = first_item_text
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = second_item_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item_text)
        self.assertEqual(second_saved_item.list, list_)
