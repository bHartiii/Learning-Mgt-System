from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from authentication.serializers import UserCreationSerializer, LoginSerializer, ResetPasswordSerializer, NewPasswordSerializer
from authentication.models import User
import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from authentication.utils import Util
from django.contrib.sites.shortcuts import  get_current_site
from django.urls import reverse
from django.conf import settings
import pyshorteners
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
            user.set_password(user_data['password'])
            user.save()

            current_site = get_current_site(request).domain
            relative_link = reverse('login')
            profile_link = 'http://'+current_site+relative_link

            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(profile_link)
            email_body = "Hii "+user.get_full_name()+'\nYou registration as student is done. \n'+'Please use this link to login: \n'+short_url+"\nUsername - "+user.username+"\nPassword - "+user.password
            data = {'email_body':email_body ,'to_email':user.email, 'email_subject':'Registration is successful!!!!!!'}
            Util.send_email(data)
        return Response({f'New {user_role} is created successfully!!!!!'}, status=status.HTTP_201_CREATED)


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = authenticate(username=user_data['username'], password=user_data['password'])
        login(request, user)
        return Response({'Succesfully logged in!!!'}, status=status.HTTP_200_OK)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):       
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email']) 
        current_site = get_current_site(request).domain
        reverse_link = reverse('new-pass')
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')
       
        shortener = pyshorteners.Shortener()
        reset_link = shortener.tinyurl.short('http://'+current_site+reverse_link+'?token='+token)
        email_body = "hii \n"+user.username+"Use this link to reset password: \n"+reset_link
        data={'email_body':email_body,'to_email':user.email,'email_subject':"Reset password Link"}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_200_OK)


class NewPassword(generics.GenericAPIView):

    serializer_class = NewPasswordSerializer
    permission_classes = (AllowAny,)
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def put(self, request):
        token = request.GET.get('token')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
 
        try:
            payload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            user.set_password(user_data['password'])
            user.save()    
            return Response({'email':'New password is created'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error':'Link is Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)  
