from django.urls import path

from superlists.lists.views import home_page

urlpatterns = [path("", home_page)]
