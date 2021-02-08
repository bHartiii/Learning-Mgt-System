from django.shortcuts import render, redirect
from rest_framework import generics, status
from django.contrib.auth import logout, login, authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.serializers import UserCreationSerializer,UpdateUserSerializer, LoginSerializer, ResetPasswordSerializer, NewPasswordSerializer
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
from authentication.permissions import IsAdmin, IsNotAthenticated, OnlyAdmin
import logging
logger = logging.getLogger('django')

class UserCreationAPIView(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let admin to create new users.
        --------
        Methods:
            post: It will create new user and send email to that user.
    """
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = UserCreationSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=self.request.user)
            user_data = serializer.data
            user_role = user_data['role']
            email = user_data['email']
        
            user = User.objects.get(email=email)
            user.set_password(user_data['password'])
            if user_role == 'Mentor' or user_role == 'Admin':
                user.is_staff = True
            user.save()
            logger.info(f"New user {user_role} is created!!!")
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')
            user_data['token'] = token
            email_data = {
                'email' : user.email,
                'reverse' : 'login',
                'token' : token,
                'message' :  "Hii "+user.get_full_name()+'\n'+'You registration as '+user_role+' is done. \n'+'Please use the following link to login. This link will be activated for 24 hrours only!!! \n'+"\nUsername - "+user.username+"\nPassword - "+user_data['password'],
                'subject' : 'Registration is successfull !!!!!',
                'site' : get_current_site(request).domain
            }
            Util.email_data_with_token(email_data)
            Util.send_email(Util.email_data_with_token(email_data))
            logger.info(f"Email is sent to the {user} !!!")
            return Response({'response':user_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            logger.info("All user records are fetched!!!")
            return Response({"response": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong!!"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    """
        Summary:
        --------
            This class will let authorized user to update and get user details.
        --------
        Methods:
            get_queryset : Admin will get all the users details.
            perform_update : Admin will able to update user details.
            perform_destroy : Admin can delete the user.
    """
    permission_classes = (IsAuthenticated, OnlyAdmin)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        try:
            logger.info(f'user {self.kwargs[self.lookup_field]} is fetched!!!')
            return self.queryset.all()
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something wrong went!!!"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            user = serializer.save(updated_by=self.request.user)
            logger.info(f"{user} details are updated!!!")
            return Response({'response': user}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        try:
            instance.delete()
            logger.info(f"{instance.id } is deleted !!!")
            return Response({'response': f'{instance.role} is deleted successfully!!!'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong !!!"}, status=status.HTTP_400_BAD_REQUEST)

class Login(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to login.
        --------
        Methods:
            post : User will able to login and create new session.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request):
        try:
            token = request.GET.get('token')
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            user = User.objects.get(username=user_data['username'])    
            if token:
                payload = jwt.decode(token, settings.SECRET_KEY)
                user_from_token = User.objects.get(id=payload['user_id'])
                if user_from_token==user and user.first_login == False:
                    user_request = authenticate(username=user_data['username'], password=user_data['password'])
                    login(request, user_request)
                    response = redirect('/auth/new-password/?token='+token)
                    user.first_login = True
                    user.save()
                    logger.info(f"{user} is logged in for first time!!!")
                    return response
                else:
                    logger.errro(f"{user} has used login link already !!!")
                    return Response({'response':'You can use this link only once !!!'}, status=status.HTTP_400_BAD_REQUEST)
            elif not token and user.first_login == False and user.is_superuser==False:
                logger.info(f"{user} need to use link sent on email for first login !!!")
                return Response({'response':'Please check your email for first login!!!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = authenticate(username=user_data['username'], password=user_data['password'])
                login(request, user)
                logger.info(f"{user} is logged in !!!")
                return Response(user_data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            logger.error("Link is expired !!!")
            return Response({'response':'Link is Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            logger.error("Invalid token !!!")
            return Response({'response':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            logger.error(e)
            return Response({'response':'Something went wrong.Please try again!!'}, status=status.HTTP_400_BAD_REQUEST)
            

class Logout(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to create and get notes.
        --------
        Methods:
            get : Session will be deleted and user will be logged out.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            logout(request)
            logger.ingo(f"{user} is logged out !!!")
            return Response({"success": "Successfully logged out."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response":"Something went wrong !!!"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let user to reset password with out login.
        --------
        Methods:
            post : User will get a new password link .
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (IsNotAthenticated,)

    def post(self, request):   
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            user = User.objects.get(email=user_data['email']) 
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')
            user_data['token'] = token
            email_data = {
                'email' : user.email,
                'reverse' : 'new-password',
                'token' : token,
                'message' :  "Hii "+user.get_full_name()+'\n'+"Use this link to reset password: \n",
                'subject' : 'Reset password Link',
                'site' : get_current_site(request).domain
            }
            Util.email_data_with_token(email_data)
            Util.send_email(Util.email_data_with_token(email_data))
            logger.info("Reset password link is sent to email !!!")
            return Response({"response":user_data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'response':'This email does not exist!!!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get a link for creating new password.
        --------
        Methods:
            post : User will get a new password link by email.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):       
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            user = User.objects.get(email=user_data['email']) 
            if user == request.user:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')
                user_data['token'] = token
                email_data = {
                    'email' : user.email,
                    'reverse' : 'new-password',
                    'token' : token,
                    'message' :  "Hii "+user.get_full_name()+'\n'+"Use this link to reset password: \n",
                    'subject' : 'Reset password Link',
                    'site' : get_current_site(request).domain
                }
                Util.email_data_with_token(email_data)
                Util.send_email(Util.email_data_with_token(email_data))
                logger.info(f"Reset password link is sent to the {user}.")
                return Response({"response":user_data}, status=status.HTTP_200_OK)
            else:
                logger.info("THis email is not registered for this account !!!")
                return Response({'response':'This email is not registered for this account!!!'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error("This email does not exist!!!")
            return Response({'response':'This email does not exist!!!'}, status=status.HTTP_400_BAD_REQUEST)

class NewPassword(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let user to create new password.
        --------
        Methods:
            put : User will create and confirm new password.
    """
    serializer_class = NewPasswordSerializer
    permission_classes = (AllowAny,)
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def put(self, request):
        try:
            token = request.GET.get('token')
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            payload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            user.set_password(user_data['password'])
            user.save()
            logger.info(f"New password is set for {user}")    
            return Response({'response':'New password is created'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            logger.error("Link is expired!!!")
            return Response({'response':'Link is Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            logger.error("Invalid token")
            return Response({'response':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            logger.error(e)
            return Response({"resposne":"Something is went wrong !!!"}, status=status.HTTP_400_BAD_REQUEST)