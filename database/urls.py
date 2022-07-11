"""database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app0 import views

urlpatterns = [
    path('', views.index),
    path('register/',views.register),
    path('logout/', views.logout),
    path('user/<str:nid>/info/', views.user_info),
    path('admin/<str:nid>/info/', views.admin_info),

    # 管理员
    path('admin_home/', views.admin_home),
    path('user/add/', views.user_add),
    path('user/<str:nid>/edit/', views.user_edit),
    path('user/<str:nid>/delete/', views.user_delete),

    path('shop/list/', views.shop_list),
    path('shop/add/', views.shop_add),
    path('shop/<str:nid>/edit/', views.shop_edit),
    path('shop/<str:nid>/delete/', views.shop_delete),

    path('item/list/', views.item_list),
    path('item/add/', views.item_add),
    path('item/<str:nid>/edit/', views.item_edit),
    path('item/<str:nid>/delete/', views.item_delete),

    path('order/list/', views.order_list),
    path('order/<str:nid>/edit/', views.order_edit),
    path('order/<str:nid>/delete/', views.order_delete),

    path('warehouse/list/', views.warehouse_list),
    path('warehouse/add/', views.warehouse_add),
    path('warehouse/<str:nid>/edit/', views.warehouse_edit),
    path('warehouse/<str:nid>/delete/', views.warehouse_delete),

    path('shop/check/list/', views.shop_check_list),
    path('shop/check/<str:nid>/edit/', views.shop_check_edit),
    path('shop/check/<str:nid>/delete/', views.shop_check_delete),

    # 用户
    path('user_home/', views.user_home),
    path('item/<str:nid>/buy/', views.item_buy),
    path('user/shop/list/', views.user_shop_list),
    path('user/shop/<str:nid>/list/', views.user_shop_item_list),
    path('user/order/list/', views.user_order_list),
    path('shop/info/', views.shop_info),
    path('shop/item/list/', views.shop_item_list),
    path('shop/item/<str:nid>/edit/', views.shop_item_edit),
    path('shop/order/list/', views.shop_order_list),
    path('order/<str:nid>/send/', views.order_send),
    path('user/shop/add/', views.user_shop_add),
    path('shop/item/add/', views.shop_item_add),
]
