# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django import forms
from .models import  CustomUser

class CustomUserForm(forms.ModelForm):
        class Meta:
                model   = CustomUser
                fields	= [ "id", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined" ]

