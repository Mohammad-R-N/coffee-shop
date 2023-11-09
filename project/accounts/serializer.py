from rest_framework import serializers
from accounts.models import User


def clean_email(value):
    forbidden_names = ["example", "email", "admin"]
    for fn in forbidden_names:
        if fn in value:
            raise serializers.ValidationError(f"{fn} can NOT be in your email")


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        escludes = ("is_active", "is_admin")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": (clean_email,)},
        }

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("passwords must match")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
