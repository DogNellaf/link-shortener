"""Содержит конфиг модуля авторизации"""
from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    """Конфиг модуля авторизации"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_auth'
    verbose_name = 'Авторизация'
