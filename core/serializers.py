from rest_framework import serializers
from core.models import User, Role, Permission


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    patronymic = serializers.CharField(max_length=50, allow_blank=True, required=False)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают")
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email уже занят")
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "patronymic"]
        read_only_fields = ["id", "email"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        