from rest_framework import serializers
from authentication.models import User

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number', 'role', 'password']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

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