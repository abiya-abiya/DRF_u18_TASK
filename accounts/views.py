from django.shortcuts import render
from rest_framework import generics

from accounts.models import CustomUser
from accounts.serializers import RegistrationSerializer


# Create your views here.

class RegisterListAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
