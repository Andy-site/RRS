from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2_boot/', views.index2_boot, name='index2_boot'),
    path('ap/', views.ap, name='ap'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('handle1/', views.handle1, name='handle1'),
    path('handle2/', views.handle2, name='handle2'),
    path('common/', views.common, name='common'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('test/', views.test, name='test'),
    path('handler/', views.handler, name='handler'),
    path('lout/', views.lout, name='lout'),
    path('lout1/', views.lout1, name='lout1'),
    path('reservation/', views.reservation, name='reservation'),
    path('manage_table/', views.manage_table, name='manage_table'),
    path('get-tables/', views.get_tables, name='get_tables'),
    path('update_table_status/', views.update_table_status, name='update_table_status'),
    path('rev123/', views.rev123, name='rev123'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('take_away/', views.take_away, name='take_away'),
    path('book/', views.book, name='book'),
    path('orders/', views.display_orders, name='display_orders'),
    path('ad/', views.order_details_view, name='order_details_view'),
    path('reviews/', views.display_reviews, name='display_reviews'),
    path('dine_in/', views.dine_in, name='dine_in'),
    path('admin_menu/', views.admin_menu, name='admin_menu'),
    path('save_order/', views.save_order, name='save_order'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('ad/', views.ad, name='ad'),
    path('admin_rev/', views.display_reviews, name='admin_rev'),







]


