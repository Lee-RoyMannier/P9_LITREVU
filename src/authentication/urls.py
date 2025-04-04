from django.urls import path
from . import views

app_name = "auth"
urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("register/", views.create_account, name="register_page"),
    path("follow/", views.follow_page, name="follow"),
    path("unfollow/<int:user_to_unfollow>/", views.unfollow_user, name="unfollow_user"),
]