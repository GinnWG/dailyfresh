from django.template.defaulttags import url

from apps.user import views
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("active/<token>", views.ActiveView.as_view(), name="active"),
    # path('user/register_handle/', views.register_handle, name='register_handle'),
]
