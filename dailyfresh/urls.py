# -*-coding:utf-8-*-
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include


from apps.user import views as user_view
from apps.goods import views as goods_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
    # path('search/', include('haystack.urls', namespace='sear')),  # 全文检索框架
    # path('user/', include('user.urls')),  # 用户模块
    # path('cart/', include('apps.cart.urls')),  # 购物车模块
    # path('order/', include('apps.order.urls')),  # 订单模块
    # path('', include('apps.goods.urls')),  # 商品模块



    # url(r'^user/$', views.register, name='register'),  # 注册页面

    path('user/', user_view.register, name='user'),
    path('goods/', goods_view.index, name='goods'),


    path('user/register/', user_view.register, name='register'),
    path('user/register_handle/', user_view.register_handle, name='register_handle'),
    path('user/login/', user_view.login, name='login'),



    path('', goods_view.index, name='index'),

]
