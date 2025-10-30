"""
URL configuration for hostel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

# --- Admin Customizations ---
admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"
# ----------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line includes the URLs from your 'hostel' app
    path('', include('hostel.urls')),
]
