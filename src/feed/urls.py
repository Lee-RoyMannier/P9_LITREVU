from django.urls import path

from . import views

app_name = "feed"
urlpatterns = [
    path("", views.home_page, name="home"),
    path("feed", views.my_post, name="my_feed"),
]