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
from users.views import login_view,logout_view, users_table, edit_user, register_user, create_group, users_in_group, delete_user, edit_group, delete_group
from contacts.views import add_contact_Detail
from django.urls import include

urlpatterns = [
    path("", index, name='index'),
    path("about/", about, name='about'),
    path('register/', register_user, name='register'),
    path('add-contact/', add_contact_Detail, name='add_contact'),
    path("users/", users_table, name='user_list'),
    path("edit-user/<int:user_id>/", edit_user, name='edit_user'),
    path("edit-role/<int:group_id>/", edit_group, name='edit_group'),
    path("delete-role/<int:group_id>/", delete_group, name='delete_group'),
    path("create_role/", create_group, name='create_group'),
    path('user/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('group/<int:group_id>/users/', users_in_group, name='users_in_group'),
    path("accounts/login/", login_view, name='login'),
    path("accounts/logout/", logout_view, name='logout'),
    path("admin/", admin.site.urls),
]
