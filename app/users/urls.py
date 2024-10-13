from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserCreateView.as_view(), name="home"),
    path("list/", views.UserListView.as_view(), name="list"),
]
