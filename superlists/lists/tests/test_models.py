from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


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

    def test_cannot_save_empty_list_item(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        list_ = List.objects.create()
        item = Item(text="", list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        """Тест получения абсолютного url"""
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

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

    def test_string_representation(self):
        """Тест строкового представления"""
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")
