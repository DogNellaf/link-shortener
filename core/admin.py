"""Модуль содержит настройки админ панели приложения"""
from django.contrib import admin
from core.models import ShortedUrl, Qr

admin.site.register(ShortedUrl)
admin.site.register(Qr)