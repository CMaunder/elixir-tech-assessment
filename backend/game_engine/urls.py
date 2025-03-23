from django.urls import path
from . import views

urlpatterns = [
    path("games/<int:game_id>", views.GameView.as_view()),
    path("games", views.GameView.as_view()),
    path("users/<int:user_id>/active-game", views.UserActiveGameView.as_view()),
    path("users", views.UserView.as_view()),
    path("users/<int:user_id>", views.UserView.as_view()),
]
