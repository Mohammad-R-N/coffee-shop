from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return f"{self.phone_number} - {self.email}"

    @property
    def is_staff(self):
        return self.is_admin


class Address(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("city",)

    def __str__(self) -> str:
        return f"{self.user} - {self.name}"


class Otp(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.phone_number} - {self.code}"
