from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import permissions
# from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token


from api.accounts.models import AccountModel
from api.accounts.serializers import AccountSerializer
from api.accounts.utils import verify_recaptcha

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# authentication_class = [JWTAuthentication]


@api_view(['POST'])
def signup_view(request): 
    serializer = AccountSerializer(data=request.data)
    if not serializer.is_valid():
        json_response = {'status': 'error', 'message': serializer.errors}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    
    # = serializer def create(self, validated_data)
    user = serializer.save()
    user.set_password(user.password)
    user.save()

    json_response = {
        'status': 'success',
        'message': 'signup successfully',
    }
    return Response(json_response, status=status.HTTP_200_OK)



@api_view(['POST'])
def login_view(request):
    account = request.data.get('account') # POST[''] # POST.get
    password = request.data.get('password')
    user = authenticate(account=account, password=password)
    if user is None:
        json_response = {'status': 'error', 'message': 'Invalid username or password'}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    # login
    login(request, user)

    json_response = {
        'status': 'success',
        'message': 'login successfully',
        'user': {
            'account': user.account,
            # 'is_superuser': user.is_superuser,
        },
        # 'jwt_token': jwt_token
    }
    return Response(json_response, status=status.HTTP_200_OK)



@api_view(['POST'])
def logout_view(request):
    logout(request) # clean auth session data
    json_response = {'status': 'success'}
    return Response(json_response, status=status.HTTP_200_OK)



