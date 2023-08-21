import logging

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, FormView
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List

User = get_user_model()
logger = logging.getLogger(__name__)


class HomePageView(FormView):
    """Представление домашней страницы"""

    template_name = "home.html"
    form_class = ItemForm


class ViewAndAddToListView(DetailView, CreateView):
    """Представления для просмотра и добавления в список элементов"""

    model = List
    template_name = "list.html"
    form_class = ExistingListItemForm

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)


class NewListView(CreateView, HomePageView):
    """Представление для нового списка"""

    form_class = NewListForm

    def form_valid(self, form: NewListForm) -> HttpResponse:
        list_ = form.save(owner=self.request.user)
        return redirect(list_)


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
