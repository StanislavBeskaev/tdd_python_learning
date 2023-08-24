import json

from django.test import TestCase

from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR
from lists.models import List, Item


class ListAPITest(TestCase):
    """Тесты API списков"""
    base_url = "/api/lists/{}/"

    def post_empty_input(self):
        list_ = List.objects.create()
        return self.client.post(self.base_url.format(list_.id), data={'text': ''})

    def test_get_returns_json_200(self):
        """Тест: возвращается ответ в формате json с кодом ответа 200"""
        list_ = List.objects.create()
        print(f"url:{self.base_url.format(list_.id)}")
        response = self.client.get(self.base_url.format(list_.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

    def test_get_returns_items_for_correct_list(self):
        """Тест: получает отклик с элементами правильного списка"""
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text="item 1")
        our_list = List.objects.create()
        item_1 = Item.objects.create(list=our_list, text="item 1")
        item_2 = Item.objects.create(list=our_list, text="item 2")
        response = self.client.get(self.base_url.format(our_list.id))

        self.assertEqual(
            json.loads(response.content.decode("utf-8")),
            [
                {"id": item_1.id, "text": item_1.text},
                {"id": item_2.id, "text": item_2.text},
            ]
        )

    def test_POSTing_a_new_item(self):
        """Тест: создание нового элемента через POST"""
        list_ = List.objects.create()
        response = self.client.post(self.base_url.format(list_.id), {"text": "new item"})

        self.assertEqual(response.status_code, 201)
        new_item = list_.item_set.get()
        self.assertEqual(new_item.text, "new item")

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_empty_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_returns_error_code(self):
        response = self.post_empty_input()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf8')), {'error': EMPTY_ITEM_ERROR})

    def test_duplicate_items_error(self):
        list_ = List.objects.create()
        self.client.post(self.base_url.format(list_.id), data={'text': 'thing'})
        response = self.client.post(self.base_url.format(list_.id), data={'text': 'thing'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf8')), {'error': DUPLICATE_ITEM_ERROR})
