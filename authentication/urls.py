from django.contrib import admin
from django.urls import path
from authentication.views import UserCreationAPIView

urlpatterns = [
    path('create-user/', UserCreationAPIView.as_view(), name='create-user'),
]
