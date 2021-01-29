from django.contrib import admin
from django.urls import path
from authentication.views import UserCreationAPIView, Login

urlpatterns = [
    path('create-user/', UserCreationAPIView.as_view(), name='create-user'),
    path('login/', Login.as_view(), name='login'),
]
