from django.urls import path
from . import views

app_name = 'segments'

urlpatterns = [
    path('', views.segment_list, name='segment_list'),
    path('<int:pk>/', views.segment_detail, name='segment_detail'),
    path('create/', views.create_segment, name='create_segment'),
]
