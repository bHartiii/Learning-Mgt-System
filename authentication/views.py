from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from authentication.serializers import UserCreationSerializer
from authentication.models import User
import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from authentication.utils import Util
from django.contrib.sites.shortcuts import  get_current_site
from django.urls import reverse
from django.conf import settings
import pyshorteners

class UserCreationAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user_role = user_data['role']
        if user_role == "Student":
            email = user_data['email']
            user = User.objects.get(email=email)
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')

            current_site = get_current_site(request).domain
            relative_link = reverse('update-details')
            profile_link = 'http://'+current_site+relative_link+"?token="+str(token)

            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(profile_link)
            email_body = "Hii "+user.get_full_name()+'\nYou registration as student is done. \n'+'Please use this link to update your details: \n'+short_url
            data = {'email_body':email_body ,'to_email':user.email, 'email_subject':'Registration is successful!!!!!!'}
            Util.send_email(data)
        return Response({'New user is created successfully!!!!!'}, status=status.HTTP_201_CREATED)

class UpdateDetails(generics.GenericAPIView):
    def get(self, request):
        pass
