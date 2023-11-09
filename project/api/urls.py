from django.urls import path
from .views import accounts_views as av
from .views import interactions_views as iv
from .views import product_views as pv
from .views import carts_views as cv


app_name = "api"
urlpatterns = [
    path("register/", av.UserRegister.as_view(), name="register-api"),
    path("userinfo/", av.UserInfo.as_view(), name="userinfo-api"),
]
