from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import List


def home_page(request: HttpRequest) -> HttpResponse:
    """Домашняя страница"""
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """Представление списка элементов"""
    list_ = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)

    return render(request, "list.html", {"list": list_, "form": form})


def new_list(request: HttpRequest) -> HttpResponse:
    """Представление для нового списка"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})
