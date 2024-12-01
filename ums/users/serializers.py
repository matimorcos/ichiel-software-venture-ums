from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user."""
    password = serializers.CharField(write_only=True)

    class Meta:
        """Meta class for RegisterSerializer."""
        model = User
        fields = [
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "birthdate",
            "country",
            "city",
            "postal_code",
            "address",
            "phone_number",
            "role",
        ]

    def create(self, validated_data):
        """Create and return a new user."""
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            birthdate=validated_data.get("birthdate"),
            country=validated_data["country"],
            city=validated_data["city"],
            postal_code=validated_data.get("postal_code"),
            address=validated_data.get("address"),
            phone_number=validated_data.get("phone_number"),
        )
        return user

class LoginSerializer(serializers.Serializer):
    """Serializer for user authentication."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate user credentials."""
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Credenciales incorrectas.")
        if not user.is_active:
            raise serializers.ValidationError("La cuenta está desactivada.")
        return {"user": user}

