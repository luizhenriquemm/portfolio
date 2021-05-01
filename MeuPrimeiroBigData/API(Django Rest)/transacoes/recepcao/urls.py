from django.urls import path
from . import views

urlpatterns = [
    path('', views.recebe_dados.as_view()),
]