from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("otp/", views.OtpView.as_view(), name="otp"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path("reset/", views.UserPasswordResetView.as_view(), name="reset_password"),
    path(
        "reset/done/",
        views.UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "confirm/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
