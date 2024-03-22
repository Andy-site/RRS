from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2_boot/', views.index2_boot, name='index2_boot'),
    path('cp/', views.cp, name='cp'),
    path('ap/', views.ap, name='ap'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('handle1/', views.handle1, name='handle1'),
    path('handle2/', views.handle2, name='handle2'),
    path('common/', views.common, name='common'),

]


