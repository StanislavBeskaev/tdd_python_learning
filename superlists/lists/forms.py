from django import forms

from lists.models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.ModelForm):
    """Форма для элемента списка"""

    class Meta:
        model = Item
        fields = ("text", )
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Enter a to-do item", "class": "form-control input-lg"})
        }
        error_messages = {
            "text": {"required": EMPTY_ITEM_ERROR}
        }

    def save(self, for_list: List):
        self.instance.list = for_list
        return super().save()
