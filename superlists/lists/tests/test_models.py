from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


User = get_user_model()


class ItemModelTest(TestCase):
    """ "Тесты модели элемента"""

    def test_default_text(self):
        """Тест заданного по умолчанию текста"""
        item = Item()
        self.assertEqual(item.text, "")

    def test_string_representation(self):
        """Тест строкового представления"""
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")


class ListAndItemModelsTest(TestCase):
    """Тест модели элемента списка"""

    def test_item_is_related_to_list(self):
        """Тест: элемент связан со списком"""
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_item(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        list_ = List.objects.create()
        item = Item(text="", list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        """Тест: повторы элементов в одном списке недопустимы"""
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="one")
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text="one")
            item.full_clean()

    def test_CAN_save_same_items_to_different_lists(self):
        """Тест: можно сохранить одинаковые элементы в разные списки"""
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        Item.objects.create(list=list_1, text="one")
        item = Item(list=list_2, text="one")
        item.full_clean()  # не должен поднять исключение

    def test_list_ordering(self):
        """Тест упорядочения списка"""
        list_1 = List.objects.create()
        item_1 = Item.objects.create(list=list_1, text="i1")
        item_2 = Item.objects.create(list=list_1, text="item 2")
        item_3 = Item.objects.create(list=list_1, text="3")

        self.assertEqual(list(Item.objects.all()), [item_1, item_2, item_3])


class ListModelTest(TestCase):
    """Тесты модели списка"""

    def test_get_absolute_url(self):
        """Тест получения абсолютного url"""
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_lists_can_have_owners(self):
        """Тест: списки могут иметь владельца"""
        user = User.objects.create(email="a@b.com")
        list_ = List.objects.create(owner=user)
        self.assertIn(list_, user.list_set.all())

    def test_list_owner_is_optional(self):
        """Тест: владелец списка является необязательным"""
        List.objects.create()  # Не должно поднимать исключение

    def test_list_name_is_first_item_text(self):
        """Тест: имя списка является текстом первого элемента"""
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="first item")
        Item.objects.create(list=list_, text="second item")
        self.assertEqual(list_.name, "first item")
