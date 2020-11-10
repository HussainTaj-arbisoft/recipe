from django import forms
from django.contrib.auth.models import User

from .models import *


class SignupForm(forms.ModelForm):
    password_confirm = forms.CharField(
        max_length=100, widget=forms.PasswordInput, required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")
        widgets = {"password": forms.PasswordInput}
        required = ("first_name", "last_name", "email", "password")

    def clean_password_confirm(self):
        p1, p2 = self.cleaned_data["password_confirm"], self.cleaned_data["password"]

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match.")

        return p1


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ("first_name", "last_name")
        required = ("first_name", "last_name")


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = False

    class Meta:
        model = Profile
        fields = ("image",)
        required = ("image",)
