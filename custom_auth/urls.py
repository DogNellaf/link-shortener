"""Конфигурация URL кастомной системы авторизации"""
from django.urls import path
import custom_auth.views as views

urlpatterns = [
    path('registration/',                      views.registration,           name="registration"),
    path('login/',                             views.login,                  name="login"),
    path('password/reset/',                    views.password_reset_request, name="password_reset_request"),
    path('password/reset/verify/',             views.password_reset_verify,  name='password_reset_verify'),
    path('password/reset/confirm/<str:code>/', views.password_reset_confirm, name='password_reset_confirm'),
]
