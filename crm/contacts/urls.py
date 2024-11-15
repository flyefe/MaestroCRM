from django.urls import path
# from . import views
from .views import create_contact, contact_list, contact_detail, delete_contact, update_contact, delete_log

#Urls patterns
urlpatterns = [
    path('update-contact/<int:contact_id>/delete', delete_contact, name='delete_contact'),
    path('update-log/<int:log_id>/delete', delete_log, name='delete_log'),
    path('update-contact/<int:contact_id>/update', update_contact, name='update_contact'),
    path('contact_deatil/<int:contact_id>/', contact_detail, name='contact_detail'),
    path('', create_contact, name='add_contact'),
    path("contact-list/", contact_list, name='contact_list'),
]



