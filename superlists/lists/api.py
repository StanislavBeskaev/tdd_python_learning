from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueTogetherValidator

from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from lists.models import List, Item


class ItemSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False, error_messages={"blank": EMPTY_ITEM_ERROR})

    class Meta:
        model = Item
        fields = ("id", "list", "text")
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=("list", "text"),
                message=DUPLICATE_ITEM_ERROR
            )
        ]


class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source="item_set")

    class Meta:
        model = List
        fields = ("id", "items",)


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


router = routers.SimpleRouter()
router.register("lists", ListViewSet)
router.register("items", ItemViewSet)
