import jwt
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.jwt import create_access_token, create_refresh_token, decode_token
from accounts.models import CustomUser
from accounts.serializers import RegistrationSerializer, LoginSerializer


# Create your views here.

class RegisterAPIView(APIView): #JWT token olish
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



class LoginAPIView(APIView):#JWT login qilish
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

class RefreshTokenAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'Error': 'Refresh token kerak'}, status=400)
        try:
            payload = decode_token(refresh_token)
            if payload['type'] != 'refresh':
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return Response({'Error': 'Refresh token eskirgan.'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'Error': 'Token yaroqsiz.'}, status=401)
        new_access = create_access_token(payload['user_id'])
        return Response({'access_token': new_access}, status=200)