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
from core.views import index, about
from users.views import login_view,logout_view, users_table, edit_user, register_user, create_group, users_in_group, UserDeleteView
from django.urls import include

urlpatterns = [
    path("", index, name='index'),
    path("about/", about, name='about'),
    path('register/', register_user, name='register'),
    path("users/", users_table, name='user_list'),
    path("edit-user/<int:user_id>/", edit_user, name='edit_user'),
    path("create_role/", create_group, name='create_group'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('group/<int:group_id>/users/', users_in_group, name='users_in_group'),
    path("accounts/login/", login_view, name='login'),
    path("accounts/logout/", logout_view, name='logout'),
    path("admin/", admin.site.urls),
]
