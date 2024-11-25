from django.urls import path
# from . import views
from .views import search_contact, filter_contact, contacts_bulk_action, create_contact, contact_list, contact_detail, delete_contact, update_contact, delete_log,update_log, contacts_by_tag,contacts_by_status, contacts_by_assigned_staff

#Urls patterns
urlpatterns = [
    path('delete-contact/<int:contact_id>/delete', delete_contact, name='delete_contact'),
    path('update-log/<int:log_id>/delete', delete_log, name='delete_log'),
    path('update-log/<int:log_id>/', update_log, name='update_log'),

    path('contacts-by-tag/<int:tag_id>/', contacts_by_tag, name='contacts_by_tag'),
    path('contacts-by-status/<int:status_id>/', contacts_by_status, name='contacts_by_status'),
    path('contacts-by-staff/<int:assigned_staff_id>/', contacts_by_assigned_staff, name='contacts_by_assigned_staff'),
    path('contact/', filter_contact, name='filter_contact'),
    path('contact-query/', search_contact, name='search_contact'),



    # path('contacts/filter/<str:filter_type>/<int:filter_id>/', filter_contacts, name='filter_contacts'),


    path('update-contact/<int:contact_id>/update', update_contact, name='update_contact'),
    path('contact_deatil/<int:contact_id>/', contact_detail, name='contact_detail'),
    path('add-contact', create_contact, name='add_contact'),
    path("contact-list/", contact_list, name='contact_list'),
    path("contacts-bulk-action/", contacts_bulk_action, name='contacts_bulk_action'),

]



