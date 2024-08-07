from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from project.serializers import ProjectSerializer


User = get_user_model()

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, max_length=15)
    address = serializers.CharField(required=False)
    #account_type = serializers.ChoiceField(choices=['basic', 'premium', 'admin'], default='basic')


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    #projects = ProjectSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'address']



###################
class CustomUserSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'user_permissions', 'groups', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
