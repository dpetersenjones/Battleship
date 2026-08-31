from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.StartGame.as_view(), name="start"),
    path('move/', views.PlayerMove.as_view(), name="move"),
    path('delete/', views.DeleteGame.as_view(), name="delete"),
]