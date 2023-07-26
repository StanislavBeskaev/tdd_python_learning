from django.urls import path
from lists import views

urlpatterns = [
    path("", views.home_page),
    path("lists/unique-list-in-world/", views.view_list),
]
