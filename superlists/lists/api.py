import json

from django.http import HttpRequest, HttpResponse

from lists.models import List


def list_handler(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    items = [{"id": item.id, "text": item.text} for item in list_.item_set.all()]

    return HttpResponse(content=json.dumps(items), content_type="application/json")
