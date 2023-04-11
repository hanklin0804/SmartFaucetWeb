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

# email SMTP
from django.core.mail import send_mail # EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import random
from django.core.cache import cache

# jwt
from rest_framework_simplejwt.tokens import RefreshToken # AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

def generate_verification_code(length=6):
    return ''.join([str(random.randint(0,9)) for _ in range(length)])

def store_verification_code(email, code): # timeout=300
    cache_key = f'verification_code_{email}'
    cache.set(cache_key, code) # timeout

def get_stored_verification_code(email):
    cache_key = f'verification_code_{email}'
    return cache.get(cache_key)

def delete_stored_verification_code(email):
    cache_key = f'verification_code_{email}'
    cache.delete(cache_key)

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

    # send email
    verification_code = generate_verification_code()
    email = serializer.validated_data['email']

    subject = 'T.A.P. verification code'
    
    message = render_to_string('email_template.txt', 
                               {'account': serializer.validated_data['account'], 'verification_code': verification_code})
    from_email = 's11a02d@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    # store 
    store_verification_code(email, verification_code)


    json_response = {
        'status': 'success',
        'message': 'signup successfully',
    }
    return Response(json_response, status=status.HTTP_200_OK)

@api_view(['POST'])
def resend_email_view(request):
    # send email
    account = request.data.get('account')
    email = request.data.get('email')
    verification_code = generate_verification_code()
    

    subject = 'T.A.P. verification code'
    
    message = render_to_string('email_template.txt', 
                               {'account': account, 'verification_code': verification_code})
    from_email = 's11a02d@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    # store 
    store_verification_code(email, verification_code)


    json_response = {
        'status': 'success',
        'message': 'resend email successfully',
    }
    return Response(json_response, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_email_verification_view(request):
    email = request.data.get('email')
    user_provided_code = request.data.get('verification_code')
    stored_verification_code = get_stored_verification_code(email)
    data={
        'user': user_provided_code,
        'stored': stored_verification_code,
    }

    if user_provided_code == stored_verification_code:
        user = AccountModel.objects.get(email=email)
        user.is_active = True
        user.save()

        delete_stored_verification_code(email)
        json_response = {'status': 'success', 'message': 'verification code successfully'}
        return Response(json_response, status=status.HTTP_200_OK)
    else:
        json_response = {'status': 'error', 'message': 'verification code error', 'data': data}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login_view(request):
    account = request.data.get('account') # POST[''] # POST.get
    password = request.data.get('password')
    user = authenticate(request, account=account, password=password)
    if user is None:
        json_response = {'status': 'error', 'message': 'Invalid username or password'}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    # login
    login(request, user)
    
    # jwt: generate 
    refresh = RefreshToken.for_user(user)
    jwt_token = {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }  
    json_response = {
        'status': 'success',
        'message': 'login successfully',
        'user': {
            'account': user.account,
            'is_superuser': user.is_superuser,
        },
        'jwt_token': jwt_token
    }
    return Response(json_response, status=status.HTTP_200_OK)



#-------------------------------------------------------------------------------#

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # jwt: delete
    refresh_token = request.data.get('refresh_token')
    token = RefreshToken(refresh_token)
    token.blacklist()

    logout(request) # clean auth session data

    json_response = {'status': 'success'}
    return Response(json_response, status=status.HTTP_200_OK)
#-------------------------------------------------------------------------------#

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def jwt_view(request):
    
    json_response = {
        'status': 'success',
        'message': 'can get data',
    }
    return Response(json_response, status=status.HTTP_200_OK)
#-------------------------------------------------------------------------------#
@api_view(['POST'])
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

#-------------------------------------------------------------------------------#
