from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,  min_length=6)
    mobile_number = serializers.RegexField("^[0-9]{10}$") 
    first_name = serializers.CharField(max_length=50,  min_length=3)
    last_name = serializers.CharField(max_length=50,  min_length=3)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number', 'role', 'password']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number', 'role', 'password']
        extra_kwargs = {'username': {'read_only': True},'password': {'read_only': True}}

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6)
    username = serializers.CharField(max_length=255, min_length=3)

    class Meta:
        model=User
        fields=['username', 'password']

    def validate(self, attrs):
        username= attrs.get('username','')
        password = attrs.get('password','')
        try:
            user = authenticate(username=username, password=password)
            if user is None:
                raise AuthenticationFailed("Invalid credentials given!!!")
        except serializers.ValidationError:
            return {'error':"Please provide email and password"}
        return attrs

class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email','')        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registerd")    
        return attrs

class NewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6)
    password2 = serializers.CharField(max_length=68, min_length=6)
        
    class Meta:
        model=User
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password','')
        password2 = attrs.get('password2','')        
        if password != password2:
            raise serializers.ValidationError("Password not matched!!")
        return attrs