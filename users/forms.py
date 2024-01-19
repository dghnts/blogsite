from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")


class CustomUserIsNotNotifyForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("is_not_notify",)
