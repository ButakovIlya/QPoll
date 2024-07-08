from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import validate_email


from .validators import *
from .utils import generate_username

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)  
    password = serializers.CharField(required=True, validators=[validate_password])  
    email = serializers.CharField(required=True, validators=[validate_email, validate_email_address])  


    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        email = validated_data.get('email')
        del(validated_data['email'])
        username = email.split('@')[0] if email else None
        username = generate_username(username)
        user = User.objects.create(
            username=username,
            email=email,
            **validated_data  
        )

        password = validated_data.get('password')
        if password:
            user.set_password(password)
            user.save()

        return user
  
    

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordCheckSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])
