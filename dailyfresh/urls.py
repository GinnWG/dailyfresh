# -*-coding:utf-8-*-
from django.contrib import admin
from django.urls import path, include


from apps.user import views as user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
    # path('search/', include('haystack.urls')),  # 全文检索框架
    # path('user/', include('user.urls')),  # 用户模块
    path('cart/', include('apps.cart.urls')),  # 购物车模块
    path('order/', include('apps.order.urls')),  # 订单模块
    path('', include('apps.goods.urls')),  # 商品模块

    # path('admin/', admin.site.urls),
    # path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
    # path('search/', include('haystack.urls')),  # 全文检索框架
    # path('user/', include('user.urls', namespace='user')),  # 用户模块
    # path('cart/', include('cart.urls', namespace='cart')),  # 购物车模块
    # path('order/', include('order.urls', namespace='order')),  # 订单模块
    # path('', include('goods.urls', namespace='goods')),  # 商品模块

    path('user/', user_view.register)
]
