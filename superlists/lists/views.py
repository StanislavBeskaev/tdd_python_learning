from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    """Домашняя страница"""
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """Представление списка элементов"""
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, "list.html", {"items": items})


def new_list(request: HttpRequest) -> HttpResponse:
    """Представление для нового списка"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get("item_text", ""), list=list_)
    return redirect(f"/lists/{list_.id}/")
