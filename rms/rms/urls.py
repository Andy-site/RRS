from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),  # Change the URL pattern name to 'login'
    path('admin_page/', views.admin_page, name='admin_page'),  # Ensure the URL pattern name is 'admin_page'
]

urlpatterns += staticfiles_urlpatterns()
