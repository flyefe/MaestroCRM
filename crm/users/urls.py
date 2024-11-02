from django.urls import path
from . import views

# from users.views import login_view,logout_view, users_table, edit_user, register_user, create_group, users_in_group, delete_user, edit_group, delete_group

#Users
urlpatterns = [
    path('register/', register_user, name='register'),
    path("users/", users_table, name='user_list'),
    path("edit-user/<int:user_id>/", edit_user, name='edit_user'),
    path("edit-role/<int:group_id>/", edit_group, name='edit_group'),
    path("delete-role/<int:group_id>/", delete_group, name='delete_group'),
    path("create_role/", create_group, name='create_group'),
    path('user/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('group/<int:group_id>/users/', users_in_group, name='users_in_group'),
    path("accounts/login/", login_view, name='login'),
    path("accounts/logout/", logout_view, name='logout'),
]