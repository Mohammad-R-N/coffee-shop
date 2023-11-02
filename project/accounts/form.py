from typing import Any
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "", "placeholder": "your password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "", "placeholder": "your password"}),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password2"] != cd["password1"]:
            raise ValidationError("PASSWORDS DO NOT MATCH")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.changed_data("password2"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="You can change password from this form <a href='../password/'>THIS FORM</a>"
    )

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "password",
            "last_login",
            "first_name",
            "last_name",
            "age",
        )


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(label="Phone Number", max_length=11)
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    age = forms.IntegerField(label="Age")
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, max_length=18
    )


class OtpForm(forms.Form):
    code = forms.IntegerField()
