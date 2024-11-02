from django.urls import path
from .views import update_statuses



urlpatterns = [
    path('update-statuses/', update_statuses, name='update_statuses'),
]