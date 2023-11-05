from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .form import UserCreationForm, UserChangeForm
from .models import User, Otp
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("phone_number", "email", "is_admin", "is_active")
    list_filter = ("is_admin", "is_active")
    readonly_fields = ("last_login",)

    fieldsets = (
        (
            "Info",
            {
                "fields": (
                    "phone_number",
                    "email",
                    "first_name",
                    "last_name",
                    "age",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "last_login",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            "Create New User",
            {
                "fields": (
                    "phone_number",
                    "email",
                    "first_name",
                    "last_name",
                    "age",
                    "password1",
                    "password2",
                )
            },
        ),
    )

    search_fields = ("email", "phone_number", "last_name")
    ordering = ("last_name", "first_name", "email")
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields["is_superuser"].disabled = True
        return form


admin.site.register(User, UserAdmin)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created")
    search_fields = ("phone_number",)
    ordering = ("created",)
