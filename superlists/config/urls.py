from accounts import urls as accounts_urls
from django.urls import include, path
from lists import urls as list_urls
from lists import views as list_views
from lists import api_urls

urlpatterns = [
    path("", list_views.HomePageView.as_view(), name="home"),
    path("lists/", include(list_urls)),
    path("accounts/", include(accounts_urls)),
    path("api/", include(api_urls)),
]
