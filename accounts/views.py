from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.jwt import create_access_token, create_refresh_token
from accounts.models import CustomUser
from accounts.serializers import RegistrationSerializer, LoginSerializer


# Create your views here.

class RegisterAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            return Response({
                "message": "Foydalanuvchi muvaffaqiyatli yaratildi",
                "user_id": user.id,
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            access = create_access_token(user.id)
            refresh = create_refresh_token(user.id)
            return Response({
                "message": "Login muvaffaqiyatli",
                "user_id": user.id,
                "access_token": access,
                "refresh_token": refresh
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Login yoki parol noto'g'ri"}, status=status.HTTP_401_UNAUTHORIZED)
