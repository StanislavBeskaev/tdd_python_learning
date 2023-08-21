import logging

from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List

User = get_user_model()
logger = logging.getLogger(__name__)


class HomePageView(FormView):
    """Представление домашней страницы"""
    template_name = "home.html"
    form_class = ItemForm


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """Представление списка элементов"""
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, "list.html", {"list": list_, "form": form})


def new_list(request):
    """Представление для нового списка"""
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def my_lists(request: HttpRequest, email: str) -> HttpResponse:
    """Представление моих списков"""
    owner = User.objects.get(email=email)
    return render(request=request, template_name="my_lists.html", context={"owner": owner})


def share_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """Представление для предоставления доступа к списку"""
    list_ = List.objects.get(id=list_id)

    shared_email = request.POST.get("sharee")
    if shared_email:
        list_.shared_with.add(shared_email)
        logger.info(f"share list {list_id} with '{shared_email}'")
    return redirect(list_)
