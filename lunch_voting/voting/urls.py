from django.urls import path
from . import views

urlpatterns = [
    path('', views.lunch_menu_view, name='lunch_menu'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]