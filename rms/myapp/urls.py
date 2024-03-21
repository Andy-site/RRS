from django.contrib import admin
from django.urls import path,include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('basic/', views.basic, name='basic'),

]

# urlpatterns += staticfiles_urlpatterns()
