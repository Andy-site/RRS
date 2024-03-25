from django.contrib import admin
from .models import MyUser123, Table


class MyUser123Admin(admin.ModelAdmin):
    list_display = ('username',)  # Display username in the list view
    search_fields = ('username',)  # Add username to search functionality


admin.site.register(MyUser123, MyUser123Admin)  # Register the model with its admin class


class TableAdmin(admin.ModelAdmin):
    list_display = ('date', 'size', 'number', 'reserved')


admin.site.register(Table, TableAdmin)  # Register the model with its admin class
