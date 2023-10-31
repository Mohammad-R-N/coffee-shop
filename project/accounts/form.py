from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserRegistrationForm(forms.Form):
    username=forms.CharField(min_length=5,label="Username",widget=forms.TextInput(attrs={"class":"","placeholder":"Hamed"}))
    email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={"class":"","placeholder":"example@email.com"}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"","placeholder":"password"}))
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"class":"","placeholder":"password"}))

    def clean_email(self):
        email=self.cleaned_data["email"]
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("this email already exists")
        return email
    
    def clean_username(self):
        username=self.cleaned_data["username"]
        user=User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("this username already exists")
        return username
    
    def clean(self) :
        cleaned_data=super().clean()
        p1=cleaned_data.get('password')
        p2=cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError("password must match")


class UserLoginForm(forms.Form):
    username=forms.CharField(min_length=5,label="Username",widget=forms.TextInput(attrs={"class":"","placeholder":"Hamed"}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"","placeholder":"password"}))