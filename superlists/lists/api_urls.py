from django.urls import path

from lists import api


urlpatterns = [
    path("lists/<int:list_id>/", api.list_, name="api_list"),
]
