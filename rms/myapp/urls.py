from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('cp/', views.cp, name='cp'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('basic/', views.basic, name='basic'),
    path('handle1/', views.handle1, name='handle1'),

]


