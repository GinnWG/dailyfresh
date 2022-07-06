from apps.user import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views
app_name = "user"
urlpatterns = [
    # path("", views.RegisterView.as_view(), name="register"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("active/<token>", views.ActiveView.as_view(), name="active"),
    path("", views.UserInfoView.as_view(), name="user"),
    path("order/", views.UserOrderView.as_view(), name="order"),
    path("address", views.AddressView.as_view(), name="address"),
    path("logout/", views.LogoutView.as_view(), name="logout")
    # path('user/register_handle/', views.register_handle, name='register_handle'),
]
