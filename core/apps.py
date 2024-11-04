"""Содержит конфиг ядра системы"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Конфиг ядра системы"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name="Линкер"
