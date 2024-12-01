from django.urls import path
from . import views

app_name = 'segments'

urlpatterns = [
    path('', views.segment_list, name='segment_list'),
    path('segment-detail/<int:pk>/', views.segment_detail, name='segment_detail'),
    path('edit-segment/<int:pk>/', views.edit_segment, name='edit_segment'),
    path('delete-segment/<int:pk>/', views.delete_segment, name='delete_segment'),
    path('create/', views.create_segment, name='create_segment'),
]
