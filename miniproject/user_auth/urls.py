from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("navbar/", views.navbar, name="navbar"),
]
