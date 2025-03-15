from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from apps.core.validators import (
    validate_email,
    validate_phone_number,
    validate_password
)
from apps.account.enums import AccountState
from apps.account.models import ArtisanProfile, Role
from apps.core.models import DataLookup
from apps.core.serializers import DataLookupSerializer


User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "code", "created_at", "updated_at"]


class UserResponseSerializer(serializers.ModelSerializer):
    state = DataLookupSerializer()
    role = RoleSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "phone_number",
            "role",
            "state",
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone_number",
            "password",
            "confirm_password",
            "role"
        ]

    def validate(self, attrs):
        validate_email(attrs.get("email"))
        validate_phone_number(attrs.get("phone_number"))
        validate_password(attrs.get("password"))

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords did not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")

        try:
            # Fetch the account state
            account_state = DataLookup.objects.get(
                type=AccountState.TYPE.value,
                value=AccountState.ACTIVE.value
            )
            # Create the user
            user = super().create(validated_data)
            user.state = account_state
            user.password = make_password(password)
            user.save()
            return user
        except DataLookup.DoesNotExist:
            raise serializers.ValidationError("Active state not found in DataLookup.")

    def to_representation(self, instance):
        return UserResponseSerializer(
            instance, self.context
        ).to_representation(instance)


class ArtisanUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone_number"
        ]


class ArtisanProfileResponseSerializer(serializers.Serializer):
    """A custom class used for swagger schema generation.
    """
    full_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    shop_name = serializers.CharField()
    profile_picture = serializers.ImageField()
    location = serializers.CharField()
    bio = serializers.CharField()


class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = ArtisanUserSerializer()

    class Meta:
        model = ArtisanProfile
        fields = [
            'user',
            'shop_name',
            'profile_picture',
            'location',
            'bio'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        validate_password(data["new_password"])
        if data["new_password"] == data["old_password"]:
            raise serializers.ValidationError(
                "You can't use the old password. please choose a new one."
            )
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
