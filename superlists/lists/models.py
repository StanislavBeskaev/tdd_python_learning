from django.db import models


class List(models.Model):
    """Список"""
    pass


class Item(models.Model):
    """Элемент списка"""

    text = models.TextField()
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
