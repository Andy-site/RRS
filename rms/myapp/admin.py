from django.contrib import admin
from .models import MyUser123, Table, Rev, Order, Food, Staff


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
    list_display = ('username', 'password')


admin.site.register(Staff, StaffAdmin)
