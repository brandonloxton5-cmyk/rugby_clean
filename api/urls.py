from django.urls import path
from . import views
from . import views_selection

urlpatterns = [
    path("", views.home, name="home"),
    path("live-board/", views.live_board, name="live_board"),

    # Fast edit board
    path("selection/", views_selection.live_selection_board, name="selection"),

    # AJAX endpoints (IMPORTANT: names used by {% url %} in template)
    path("selection/assign/", views_selection.assign_player, name="assign_player"),
    path("selection/clear/", views_selection.clear_slot, name="clear_slot"),
]
