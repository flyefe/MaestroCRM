from django.urls import path
# from . import views
from .views import add_contact_detail, contact_list, contact_detail, update_contact, delete_contact

#Urls patterns
urlpatterns = [
    path('update-contact/<int:contact_id>/delete', delete_contact, name='delete_contact'),
    path('update-contact/<int:contact_id>/update', update_contact, name='update_contact'),
    path('contact_deatil/<int:contact_id>/', contact_detail, name='contact_detail'),
    path('add-contact/', add_contact_detail, name='add_contact'),
    path("contact-list/", contact_list, name='contact_list'),
]



