from django.urls import path
# from . import views
from . import views

#Urls patterns
urlpatterns = [
    path('delete-contact/<int:contact_id>/delete', views.delete_contact, name='delete_contact'),
    path('update-log/<int:log_id>/delete', views.delete_log, name='delete_log'),
    path('update-log/<int:log_id>/', views.update_log, name='update_log'),

    path('contacts-by-tag/<int:tag_id>/', views.contacts_by_tag, name='contacts_by_tag'),
    path('contacts-by-status/<int:status_id>/', views.contacts_by_status, name='contacts_by_status'),
    path('contacts-by-staff/<int:assigned_staff_id>/', views.contacts_by_assigned_staff, name='contacts_by_assigned_staff'),
    path('contacts-trafick-source/<int:trafick_source_id>/', views.contacts_by_trafick_source, name='contacts_by_trafick_source'),
    path('contact/', views.filter_contact, name='filter_contact'),
    path('contact-query/', views.search_contact, name='search_contact'),



    # path('contacts/filter/<str:filter_type>/<int:filter_id>/', filter_contacts, name='filter_contacts'),


    path('update-contact/<int:contact_id>/update', views.update_contact, name='update_contact'),
    path('contact_deatil/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('add-contact', views.create_contact, name='add_contact'),
    path("contact-list/", views.contact_list, name='contact_list'),
    path("contacts-bulk-action/", views.contacts_bulk_action, name='contacts_bulk_action'),

]



