from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from authentication.serializers import UserCreationSerializer
from authentication.models import User

class UserCreationAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = User.objects.create()
        user.save()
        return Response({'New user is created successfully!!!!!'})