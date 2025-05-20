from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('loader/', views.loader_view, name='loader'),
    path('menu/', views.menu_view, name='menu'),
    path('order/', views.order_view, name='order'),
]

