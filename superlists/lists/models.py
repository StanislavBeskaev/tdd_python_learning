from django.db import models
from django.urls import reverse


class List(models.Model):
    """Список"""

    def get_absolute_url(self) -> str:
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    """Элемент списка"""

    text = models.TextField()
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
