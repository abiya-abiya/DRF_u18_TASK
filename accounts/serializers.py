from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.models import CustomUser
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
    write_only=True, validators=[validate_password],
)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'password']
        read_only_fields = ['id']
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'avatar']