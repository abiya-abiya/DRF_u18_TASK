from rest_framework import serializers

from accounts.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password',
            'phone',
        ]
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

