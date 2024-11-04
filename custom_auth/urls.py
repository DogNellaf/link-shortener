"""Конфигурация URL кастомной системы авторизации"""
from django.urls import path
import custom_auth.views as views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('registration/',   views.registration,   name="registration"),
    path('login/',          views.login,          name="login"),
    path('password/reset/', views.reset_password, name="password_reset"),
]
