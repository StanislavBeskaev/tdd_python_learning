from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest) -> HttpResponse:
    """Домашняя страница"""
    return render(
        request,
        "home.html",
        {"new_item_text": request.POST.get("item_text", "")}
    )
