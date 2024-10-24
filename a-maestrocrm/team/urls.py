from django.urls import path

from . import views

app_name = 'team'

urlpatterns = [
    path('add-member/<int:user_id>/', views.add_member_to_team, name='add_to_team'),
    path('<int:pk>/edit-team/', views.edit_team, name='edit'),
    path('remove-member/<int:user_id>/', views.remove_team_member, name='remove_member'),
    # path('client/', views.client_list, name='client_list'),
    path('add-member/', views.add_team_member, name='add_member'),
]