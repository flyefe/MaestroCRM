from django.urls import path
from .views import update_settings



urlpatterns = [
    path('update_settings/', update_settings, name='update_settings'),
]