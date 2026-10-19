from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from accounts.serializers import RegistrationSerializer, LoginSerializer


# Create your views here.

class RegisterListAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

class LoginListAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({"message": "Login muvaffaqiyatli", "user_id": user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Login yoki parol noto'g'ri"}, status=status.HTTP_401_UNAUTHORIZED)