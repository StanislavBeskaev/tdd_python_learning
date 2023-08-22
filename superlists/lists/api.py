from django.http import HttpRequest, HttpResponse


def list_(request: HttpRequest, list_id: int) -> HttpResponse:
    return HttpResponse(content_type="application/json")
