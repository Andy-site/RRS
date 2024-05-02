from django.contrib import admin
from .models import MyUser123, Table, Rev, Order, Food, Staff, DineInOrderItem, DineInOrder, Order123


class MyUser123Admin(admin.ModelAdmin):
    list_display = ('username',)  # Display username in the list view
    search_fields = ('username',)  # Add username to search functionality


admin.site.register(MyUser123, MyUser123Admin)  # Register the model with its admin class


class TableAdmin(admin.ModelAdmin):
    list_display = ('date', 'size', 'number', 'reserved')


admin.site.register(Table, TableAdmin)  # Register the model with its admin class


class RevAdmin(admin.ModelAdmin):
    list_display = ('username', 'text')


admin.site.register(Rev, RevAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'number_of_people', 'message')


admin.site.register(Order, OrderAdmin)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('type', 'food', 'price')


admin.site.register(Food, FoodAdmin)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'role')


admin.site.register(Staff, StaffAdmin)


class DineInOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'food', 'quantity', 'created_at', 'updated_at')


admin.site.register(DineInOrderItem, DineInOrderItemAdmin)


class DineInOrderAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'created_at', 'updated_at')


admin.site.register(DineInOrder, DineInOrderAdmin)


class Order123Admin(admin.ModelAdmin):
    list_display = ('items', 'pickup_time', 'pickup_location', 'order_number', 'created_at', 'updated_at',
                    'user_name', 'status', 'total', 'is_paid', 'paid_amount')


admin.site.register(Order123, Order123Admin)


