from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('<int:pk>/details/', views.client_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_client, name='edit'),
    path('<int:pk>/delete/', views.ClientDeleteView.as_view(), name='delete'),
    path('comment/<int:pk>/edit/', views.CommentEditView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),

    path('client/', views.client_list, name='list'),
    path('assigned/', views.client_assigned, name='assigned'),
    path('add_client/', views.add_client, name='add'),
]

