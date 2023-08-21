from django.urls import path
from lists import views

urlpatterns = [
    path("new", views.NewListView.as_view(), name="new_list"),
    path("<int:pk>/", views.ViewAndAddToListView.as_view(), name="view_list"),
    path("users/<str:email>/", views.my_lists, name="my_lists"),
    path("<int:list_id>/share", views.share_list, name="share_list"),
]
