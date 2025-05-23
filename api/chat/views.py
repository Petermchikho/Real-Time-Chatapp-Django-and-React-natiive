from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,SignUpSerializer
# Create your views here.

def get_auth_for_user(user):
    refresh= RefreshToken.for_user(user)
    
    return {
        'user':UserSerializer(user).data,
        'tokens':{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }
class SignInView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        username = request.data.get("username", "").strip()  # Trim spaces
        password = request.data.get("password", "").strip()
        if not username or not password:
            return Response(status=400)
        
        user = authenticate(username=username, password=password)

        if not user:
            return Response(status=401)
        
        user_data = get_auth_for_user(user)

        return Response(user_data) 

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        new_user=SignUpSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        user = new_user.save()

        user_data = get_auth_for_user(user)

        return Response(user_data)