from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import Register_serializer, Login_serializer





class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        requested_data = request.data
        serializer = Login_serializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        username = data.get('username')
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            if not User.objects.filter(username=username).first():
                error={"error": "No username found"}
                return Response(error,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            return super(LoginAPI, self).post(request, format=None)
        except Exception as e:
            error={"error": "password is incorrect"}
            return Response(error,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class Register(APIView):
    def register(self,email,username,password):
        try:
            if User.objects.filter(email=email).first():
                error = {"Error": "Email Already Exists"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).first():
                error = {"Error": "Username Already Exists"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        requested_data = request.data
        serializer = Register_serializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        username=data.get('username')
        email=data.get('email')
        password = data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password == confirm_password:
            self.register(email,username,password)
            return JsonResponse("successfully created user", safe=False)
        else:
            error={"Error": "Passwords doesn't matched"}
            return Response(error,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)