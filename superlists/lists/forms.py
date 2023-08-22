from django import forms
from django.core.exceptions import ValidationError
from lists.models import Item, List

DUPLICATE_ITEM_ERROR = "You've already got this in your list"
EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.ModelForm):
    """Форма для элемента списка"""

    class Meta:
        model = Item
        fields = ("text",)
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Enter a to-do item", "class": "form-control input-lg"})
        }
        error_messages = {"text": {"required": EMPTY_ITEM_ERROR}}

    def save(self, for_list: List):
        self.instance.list_ = for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    """Форма для элемента существующего списка"""

    def __init__(self, for_list: List, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list_ = for_list

    def validate_unique(self):
        """Проверка уникальности для элементов списка"""
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {"text": [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.ModelForm.save(self)


class NewListForm(ItemForm):
    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])
