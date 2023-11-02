from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import UserRegistrationForm
from utils import send_otp
from .models import Otp
import random
from django.contrib import messages


class UserRegistrationView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/registration.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            random_code = random.randint(1000, 9999)
            cd = form.cleaned_data
            send_otp(cd["phone_number"], random_code)
            print(f"####### OTP CODE IS {random_code} #######")
            Otp.objects.create(phone_number=cd["phone_number"], code=random_code)
            request.session["user_registration"] = {
                "phone_number": cd["phone_number"],
                "email": cd["email"],
                "first_name": cd["first_name"],
                "last_name": cd["last_name"],
                "age": cd["age"],
                "password": cd["password"],
            }
            # request.session.modified = True
            messages.success(request, "OTP CODE SENT...", "success")
            return redirect("accounts:otp")
        messages.success(request, "Something was Wrong", "danger")
        return redirect("core:home-page")
