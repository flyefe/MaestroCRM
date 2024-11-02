from django.urls import path
# from . import views
from .views import add_contact_detail, contact_list,update_contact_detail

#Urls patterns
urlpatterns = [
    path('update-contact/<int:contact_id>/', update_contact_detail, name='update_contact'),
    path('add-contact/', add_contact_detail, name='add_contact'),
    path("contact-list/", contact_list, name='contact_list'),
]



