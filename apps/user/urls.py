from apps.user import views
from django.urls import path, include

urlpatterns = [
    path(r'^register$', views.register, name='register'),
    path(r'^register_handle', views.register_handle, name='register_handle'),
]
