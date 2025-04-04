from django.urls import path
from . import views

app_name = "ticket"
urlpatterns = [
    path("create-ticket", views.create_ticket, name="create_ticket"),
    path("edit-ticket/<int:id_ticket>/", views.edit_ticket, name="edit_ticket"),
    path("delete-ticket/<int:id_ticket>/", views.delete_ticket, name="delete_ticket"),
]