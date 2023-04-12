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

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# authentication_class = [JWTAuthentication]
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@csrf_exempt
def signup_view(request): 
    serializer = AccountSerializer(data=request.data)
    if not serializer.is_valid():
        json_response = {'status': 'error', 'message': serializer.errors}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    
    # = serializer def create(self, validated_data)
    user = serializer.save()
    user.set_password(user.password)
    user.is_active = 1
    user.save()

    json_response = {
        'status': 'success',
        'message': 'signup successfully',
    }
    return Response(json_response, status=status.HTTP_200_OK)

import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    account = request.data.get('account') # POST[''] # POST.get
    password = request.data.get('password')
    user = authenticate(account=account, password=password) #request, 
    if user is None:
        logger.error('Invalid username or password')
        json_response = {'status': 'error', 'message': 'Invalid username or password'}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    # login
    login(request, user)

    json_response = {
        'status': 'success',
        'message': 'login successfully',
        'user': {
            'account': user.account,
            'is_superuser': user.is_superuser,
        },
        # 'jwt_token': jwt_token
    }
    return Response(json_response, status=status.HTTP_200_OK)



@api_view(['POST'])
@csrf_exempt
def logout_view(request):
    logout(request) # clean auth session data
    json_response = {'status': 'success'}
    return Response(json_response, status=status.HTTP_200_OK)



@api_view(['POST'])
@csrf_exempt
def add_default_users_view(request): 
    for i in range(1, 11):
        data = {"account": f"user{i}", "email": f"user{i}@gmail.com", "name": f"user{i}", "password": "1234", "phone": "1234"}
        serializer = AccountSerializer(data=data)
        if not serializer.is_valid():
            json_response = {'status': 'error', 'message': serializer.errors}
            return Response(json_response, status=status.HTTP_404_NOT_FOUND)
        user = serializer.save()
        user.set_password(user.password)
        user.save()
    
    json_response = {
        'status': 'success',
        'message': 'default user1-10 created successfully (password=1234)',
    }
    return Response(json_response, status=status.HTTP_200_OK)