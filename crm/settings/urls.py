from django.urls import path
from . import views



urlpatterns = [
    path('update-settings/', views.update_settings, name='update_settings'),
    # path('status-settings/', views.update_status, name='status_settings'),

]