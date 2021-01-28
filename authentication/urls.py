from django.contrib import admin
from django.urls import path
from authentication.views import UserCreationAPIView, UpdateDetails

urlpatterns = [
    path('create-user/', UserCreationAPIView.as_view(), name='create-user'),
    path('update-deatils/', UpdateDetails.as_view(), name='update-details'),
]
