from django.urls import path
from . import views

app_name = "bulletin"

urlpatterns = [
    path("", views.board, name="board"),
    path("add/", views.add_item, name="add"),
    path("done/<int:pk>/", views.mark_done, name="done"),
    path("delete/<int:pk>/", views.delete_item, name="delete"),
]
