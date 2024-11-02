from django.urls import path
# from . import views
from .views import add_contact_Detail, contact_list

#Urls patterns
urlpatterns = [
    path('add-contact/', add_contact_Detail, name='add_contact'),
    path("contact-list/", contact_list, name='contact_list'),
]



