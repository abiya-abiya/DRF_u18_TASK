from django.contrib import admin
from django.urls import path, include

from accounts.views import RegisterListAPIView, LoginListAPIView

urlpatterns = [
    path('register/', RegisterListAPIView.as_view()),
    path('login/', LoginListAPIView.as_view()),
]