from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    """Домашняя страница"""
    return render(request, "home.html")


def view_list(request: HttpRequest) -> HttpResponse:
    """Представление списка элементов"""
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})


def new_list(request: HttpRequest) -> HttpResponse:
    """Представление для нового списка"""
    Item.objects.create(text=request.POST.get("item_text", ""))
    return redirect("/lists/unique-list-in-world/")
