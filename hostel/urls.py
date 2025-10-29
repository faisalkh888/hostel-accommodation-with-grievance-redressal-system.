from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# This file maps URLs to your view functions. It is essential for the app to work.
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('grievances/', views.grievances, name='grievances'),
    path('grievances/create/', views.create_grievance, name='create_grievance'),
    path('grievances/status/<int:grievance_id>/', views.get_grievance_status, name='get_grievance_status'),
    path('grievances/update/<int:grievance_id>/', views.update_grievance_status, name='update_grievance_status'),
]

