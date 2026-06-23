"""
Конфигурация URL для взаимодейстия с аккаунтом
"""
from django.urls import path
from account import views

urlpatterns = [
    path('',                views.account,                 name="account"),
    path('avatar/remove',   views.avatar_remove,           name="avatar_remove"),
    path('avatar/update',   views.avatar_update,           name="avatar_update"),
    path('update',          views.account_update_data,     name="account_update_data"),
    path('password/update', views.account_update_password, name="account_update_password"),
    path('price',           views.account_price,           name="account_price"),
    path('password',        views.account_password,        name="account_password"),
]
