from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Daily Task Manager Admin"
admin.site.site_title = "Daily Task Manager Admin Protal"
admin.site.index_title = "Welcome to Daily Task Manager"



urlpatterns = [path('admin/', admin.site.urls), 
               path('', include('ship.urls'))]
