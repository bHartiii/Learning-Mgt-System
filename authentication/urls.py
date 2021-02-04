from django.contrib import admin
from django.urls import path
from authentication.views import UserCreationAPIView, UserDetails, Login,Logout, ForgotPassword, ResetPassword, NewPassword

urlpatterns = [
    path('user/', UserCreationAPIView.as_view(), name='create-user'),
    path('user/<int:id>', UserDetails.as_view(), name='user'),
    path('login/', Login.as_view(), name='login'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot-password'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('new-password/', NewPassword.as_view(), name='new-password'),
    path('logout/', Logout.as_view(), name='logout'),
]
