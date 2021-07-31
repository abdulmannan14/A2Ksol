
from rest_framework import serializers
from .models import User


class Register_serializer(serializers.Serializer):
    email = serializers.EmailField()
    username=serializers.CharField(max_length=20)
    password= serializers.CharField(max_length=15,min_length=8)
    confirm_password=serializers.CharField(max_length=15,min_length=8)


class Login_serializer(serializers.Serializer):
    username=serializers.CharField(max_length=20)
    password= serializers.CharField(max_length=15,min_length=8)

