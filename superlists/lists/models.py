from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class List(models.Model):
    """Список"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name="shared")

    def get_absolute_url(self) -> str:
        return reverse("view_list", args=[self.id])

    @property
    def name(self) -> str:
        """Имя"""
        return self.item_set.first().text

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_


class Item(models.Model):
    """Элемент списка"""

    text = models.TextField()
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self):
        return self.text
