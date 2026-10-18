from django.contrib import admin
from django.urls import path, include

from accounts.views import RegisterListAPIView

urlpatterns = [
    path('register/', RegisterListAPIView.as_view()),
]