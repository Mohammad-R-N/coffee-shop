from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("otp/", views.OtpView.as_view(), name="otp"),
]
