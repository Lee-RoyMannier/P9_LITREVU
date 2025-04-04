from django.urls import path

from . import views

app_name = "review"
urlpatterns = [
    path("create-review/", views.create_review, name="create-review"),
    path("review/<int:ticket_id>/", views.respond_to_ticket, name="review"),
    path("review/<int:review_id>/update/", views.update_review, name="update_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),

]