from django.template.defaulttags import url

from apps.user import views
from django.urls import path, include
from apps.user.views import RegisterView

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='register'),
    # path('user/register_handle/', views.register_handle, name='register_handle'),
]
