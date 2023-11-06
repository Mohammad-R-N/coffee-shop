from typing import Any
from django import forms
from .models import User, Otp
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
        user.set_password(self.cleaned_data["password2"])
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
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=11,
        widget=forms.TextInput(attrs={"class": "inputBox1"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "inputBox1"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
    )
    age = forms.IntegerField(label="Age")
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "inputBox"}),
        max_length=18,
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email already exists")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError("This phone number already exists")
        Otp.objects.filter(phone_number=phone_number).delete()
        return phone_number


class OtpForm(forms.Form):
    code = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "btn btn-outline-warning text-dark user",
                "style": "height: 50px; width:200px;",
            }
        )
    )


class UserLoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
