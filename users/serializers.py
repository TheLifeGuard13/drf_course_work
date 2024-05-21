from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "is_superuser",
            "is_staff",
            "is_active",
            "email",
            "groups",
            "password",
        )
