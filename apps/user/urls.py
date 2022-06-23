from django.template.defaulttags import url

from apps.user import views
from django.urls import path, include

urlpatterns = [
    path('user/register/', views.register, name='register'),
    path('user/register_handle/', views.register_handle, name='register_handle'),
]
