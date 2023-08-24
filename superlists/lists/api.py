import json

from django.http import HttpRequest, HttpResponse

from lists.forms import ExistingListItemForm
from lists.models import List


def list_handler(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(
                content=json.dumps({'error': form.errors['text'][0]}),
                content_type='application/json',
                status=400
            )

    items = [{"id": item.id, "text": item.text} for item in list_.item_set.all()]
    return HttpResponse(content=json.dumps(items), content_type="application/json")
