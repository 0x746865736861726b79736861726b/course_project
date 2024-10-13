from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="list"),
    path("create/", views.UserCreateView.as_view(), name="create"),
    path("auth/", views.AuthenticateUserView.as_view(), name="auth"),
]
