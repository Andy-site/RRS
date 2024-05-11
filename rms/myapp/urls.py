from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ap/', views.ap, name='ap'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('handle1/', views.handle1, name='handle1'),
    path('handle2/', views.handle2, name='handle2'),
    path('common/', views.common, name='common'),
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
    path('dine_in/', views.dine, name='dine_in'),
    path('admin_menu/', views.admin_menu, name='admin_menu'),
    path('save_order/', views.save_order, name='save_order'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('ad/', views.ad, name='ad'),
    path('admin_rev/', views.display_reviews, name='admin_rev'),
    path('add-tables/', views.add_tables_for_30_days, name='add_tables_for_30_days'),
    path('foods/', views.dine, name='dine'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('send_confirmation_email/', views.send_confirmation_email, name='send_confirmation_email'),
    path('send_sorry_email/', views.send_sorry_email, name='send_sorry_email'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dine-in-details/', views.dine_in_details, name='dine_in_details'),
    path('complete_orders/', views.complete_orders, name='complete_orders'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('place_order/', views.place_order, name='place_order'),
    path('get_order_history/', views.get_order_history, name='get_order_history'),
    path('cancel-order/<str:order_number>/', views.cancel_order_takeaway, name='cancel_order_takeaway'),
    path('take_away_admin/', views.admin_orders, name='take_away_admin'),
    path('cancel-order-ta/', views.cancel_order_ta, name='cancel_order_ta'),
    path('complete-order-ta/', views.complete_order_ta, name='complete_order_ta'),
    path('esewa/', views.esewa, name='esewa'),
    path('orders69/<int:id>/', views.orders69, name='orders69'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('esewa-callback/', views.esewa_callback_view, name='esewa_callback'),
    path('order_now/', views.order_now, name='order_now'),





]

