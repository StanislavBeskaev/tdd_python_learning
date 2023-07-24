from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
    """Домашняя страница"""
    return HttpResponse("<html><title>To-Do lists</title></html>")
