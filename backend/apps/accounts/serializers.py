from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source="profile.display_name", allow_blank=True, required=False)
    timezone = serializers.CharField(source="profile.timezone", required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "display_name", "timezone")
        read_only_fields = ("id", "username")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    display_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm", "display_name")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        display_name = validated_data.pop("display_name", "")
        user = User.objects.create_user(**validated_data)
        user.profile.display_name = display_name
        user.profile.save(update_fields=["display_name", "updated_at"])
        return user
