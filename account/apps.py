"""Настройки приложения аккаунтов"""
from django.apps import AppConfig


class AccountConfig(AppConfig):
    """Конфиг приложения аккаунтов"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = "Аккаунт"
