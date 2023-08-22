import json

from django.test import TestCase

from lists.models import List, Item


class ListAPITest(TestCase):
    """Тесты API списков"""
    base_url = "/api/lists/{}/"

    def test_get_returns_json_200(self):
        """Тест: возвращается ответ в формате json с кодом ответа 200"""
        list_ = List.objects.create()
        print(f"url:{self.base_url.format(list_.id)}")
        response = self.client.get(self.base_url.format(list_.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
