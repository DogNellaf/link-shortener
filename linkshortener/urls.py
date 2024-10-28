"""
URL configuration for linkshortener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import core.views as core_views
import custom_auth.views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', core_views.index, name = "index"),
    path('linker', core_views.linker, name = "linker"),
    path('linker/create', core_views.generate_url, name="generate_url"),
    path('linker/<str:url>', core_views.linker, name = "linker_with_url"),
    path('qr', core_views.qr_generator, name = "qr_generator"),
    path('history', core_views.history, name = "history"),
    path('price', core_views.price, name = "price"),
    path('account', core_views.account, name = "account"),
    path('account/data/update', core_views.account_update_data, name="account_update_data"),
    path('account/password/update', auth_views.account_update_password, name="account_update_password"),
    path('account/price', core_views.account_price, name = "account_price"),
    path('account/password', core_views.account_password, name = "account_password"),
    path('privacy', core_views.privacy, name = "privacy"),
    # path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', auth_views.registration, name = "registration"),
    path('auth/login/', auth_views.login, name="login"),
    path('auth/password/reset', auth_views.reset_password, name="password_reset"),
    path('<str:url>', core_views.redirect_to_url, name = "redirect_to_url"),
]
