from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("otp/", views.OtpView.as_view(), name="otp"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
]
