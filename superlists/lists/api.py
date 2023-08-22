import json

from django.http import HttpRequest, HttpResponse

from lists.models import List, Item


def list_handler(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        Item.objects.create(list=list_, text=request.POST["text"])
        return HttpResponse(status=201)

    items = [{"id": item.id, "text": item.text} for item in list_.item_set.all()]
    return HttpResponse(content=json.dumps(items), content_type="application/json")
