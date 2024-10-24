from django.contrib import admin

from .models import Client, ClientComment

# Register your models here.
admin.site.register(Client)
admin.site.register(ClientComment)

