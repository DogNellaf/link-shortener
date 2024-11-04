"""Модуль содержит настройки админ панели приложения"""
from django.contrib import admin
from core.models import ShortedUrl

admin.site.register(ShortedUrl)
