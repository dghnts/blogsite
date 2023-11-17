# Register your models here.
# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/== #

from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display	= ["username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined" ]

admin.site.register(CustomUser,CustomUserAdmin)