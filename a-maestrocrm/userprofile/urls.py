from django.urls import path

from . import views


app_name = 'userprofiles'

urlpatterns = [
    path('myaccount/', views.myaccount, name='myaccount'),
    path('error/', views.error, name='error'),
    path('sign-up/', views.signup, name='signup'),
]