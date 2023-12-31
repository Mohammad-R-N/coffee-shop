from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, phone_number, email, password, first_name=None, last_name=None, age=None
    ):
        if not phone_number:
            raise ValueError("User should have a phone number")

        if not email:
            raise ValueError("User should have an email")

        user = self.model(phone_number=phone_number, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password):
        user = self.create_user(phone_number, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
