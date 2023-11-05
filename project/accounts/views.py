from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .form import UserRegistrationForm, OtpForm, UserLoginForm
from utils import send_otp
from .models import Otp, User
import random


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/registration.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

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
        return render(request, self.template_name, {"form": form})


class OtpView(View):
    form_class = OtpForm
    template_name = "accounts/otp.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user_session = request.session["user_registration"]
        otp_instance = Otp.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["code"] == otp_instance.code:
                User.objects.create_user(
                    phone_number=user_session["phone_number"],
                    email=user_session["email"],
                    first_name=user_session["first_name"],
                    last_name=user_session["last_name"],
                    age=user_session["age"],
                    password=user_session["password"],
                )
                otp_instance.delete()
                messages.success(request, "YOU REGISTERED.", "success")
                return redirect("core:home-page")
            else:
                messages.error(request, "THIS CODE IN WRONG!", "warning")
                return redirect("accounts:otp")
        return redirect("core:home-page")


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd["phone_number"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "you logged in successfully", "info")
                return redirect("core:home-page")
            messages.error(request, "phone or password is wrong", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "you logged out successfully", "success")
        return redirect("core:home-page")


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/reset_password.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    email_template_name = "accounts/email_reset_password.html"
