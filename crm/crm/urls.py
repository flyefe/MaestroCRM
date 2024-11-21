"""
URL configuration for crm project.

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
from django.urls import path
from core.views import index, about, sign_up, login_view, logout_view, permission_denied
from django.urls import include

urlpatterns = [
    
    #Django Admin
    path("admin-site/", admin.site.urls),

    #Public-facing URl
    path("", index, name='index'),
    path("about/", about, name='about'),
    path("permission-denied/", permission_denied, name='permission_denied'),
    path("accounts/login/", login_view, name='login'),
    path('sign-up/', sign_up, name='sign_up'),
    path("accounts/logout/", logout_view, name='logout'),


    #INCLUDE
    #Backend URLs (admin view)
    path('admin/contacts/', include('contacts.urls')),
    path('admin/user/', include('users.urls')),
    path('admin/settings/', include('settings.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),

    ]
