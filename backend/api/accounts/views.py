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

# from rest_framework_simplejwt.views
# from rest_framework_simplejwt.token_blacklist import views as jwt_views
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
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin # AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
import jwt

# csrf
from django.views.decorators.csrf import csrf_exempt
# def generate_verification_code(length=6):
#     return ''.join([str(random.randint(0,9)) for _ in range(length)])

# def store_verification_code(email, code): # timeout=300
#     cache_key = f'verification_code_{email}'
#     cache.set(cache_key, code) # timeout

from django.contrib.auth.models import Group


# class CacheManager:
#     def store_to_cache(stored_type: str, stored_id: str, stored_data: str, stored_time: int) -> int:
#         cache_key = f'{stored_type}_{stored_id}'
#         cache.set(cache_key, stored_data, stored_time)
#     def delete_from_cache(stored_type: str, stored_id: str, stored_data: str) -> int:
#         cache_key = f'{stored_type}_{stored_id}'
#         cache.delete(cache_key, stored_data)
#     def get_from_cache(stored_type: str, stored_id: str) -> int:
#         cache_key = f'{stored_type}_{stored_id}'
#         return cache.get(cache_key)



def store_signup_account(json_data):
    print(json_data)
    account = json_data['account']
    cache_key = f'signup_account_{account}'
    cache.set(cache_key, json_data, 20)
    
def get_stored_signup_account(account):
    cache_key = f'signup_account_{account}'
    json_data = cache.get(cache_key)    
    return json_data

def get_stored_verification_code(email) :
    cache_key = f'verification_code_{email}'
    return cache.get(cache_key)

def delete_stored_verification_code(email):
    cache_key = f'verification_code_{email}'
    cache.delete(cache_key)

def send_email_verification_code(account, email):
    # generate
    verification_code = ''.join([str(random.randint(0,9)) for _ in range(6)])
    # send
    subject =  'T.A.P. verification code'
    message = render_to_string('email_template.txt', {'account': account, 'verification_code': verification_code})
    from_email = 's11a02d@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    # store
    cache_key = f'verification_code_{email}'
    cache.set(cache_key, verification_code)

def add_count_in_cache(type, item):
    cache_key = f'{type}_{item}'
    count = cache.get_or_set(cache_key, 0)
    count += 1
    cache.set(cache_key, count)
    return count

def count_limit(type, item, limit):
    cache_key = f'{type}_{item}'
    count = cache.get(cache_key)
    if count is not None and count >= limit:
        return False
    return True

#-------------------------------------------------------------------------------#
# def encode_jwt(payload, secret_key):
#     return jwt.encode(payload, secret_key, algorithm='HS256')
# def decode_jwt(jwt_string, secret_key):
#     try:
#         payload = jwt.decode(jwt_string, secret_key, algorithms=['HS256'])
#         return payload
#     except:
#         return ''


#-------------------------------------------------------------------------------#
import json
import logging
logger = logging.getLogger(__name__)
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def test(request):
    serializer = AccountSerializer(data=request.data)
    # store_signup_account(serializer)
    if not serializer.is_valid():
        json_response = {'status': 'error', 'message': serializer.errors}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    store_signup_account(request.data)
    # user = serializer.save()
    # user.data
    # serializer.get_fields()
    # logger.info('ssssssss')
    # json_response = {type(serializer)}
    # print(type(serializer))
    return Response({'a': request.data}, status=status.HTTP_200_OK)

#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def signup_view(request): 
    serializer = AccountSerializer(data=request.data)
    if not serializer.is_valid():
        json_response = {'status': 'error', 'message': serializer.errors}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    
    # = serializer def create(self, validated_data)
    # user = serializer.save() # return object instance 
    # user.set_password(user.password)
    # user.is_active = False
    # group = Group.objects.get(name='Engineers')
    # group.uer_set.add(user)
    # user.save()

    send_email_verification_code(serializer.data['account'], serializer.data['email'])

    json_response = {
        'status': 'success',
        'message': 'signup & send email verification  successfully',
        'account': serializer.data['account'],
    }
    return Response(json_response, status=status.HTTP_200_OK)
#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) #?
def resend_email_verification_view(request):
    # if is_active = True 
    #   not do anything
    try:
        account = request.data.get('account')
        email = AccountModel.objects.get(account=account).email
        if count_limit('emailverification_times', account, 2) == True:
            count = add_count_in_cache('emailverification_times', account)
            send_email_verification_code(account, email)
            json_response = {
                'status': 'success',
                'message': 'resend email verification successfully',
                'error times': count
            }
            return Response(json_response, status=status.HTTP_200_OK)
        else:
            json_response = {'status': 'error', 'message': 'send email times over 3, resend email need to wait 5 mins'}
            return Response(json_response, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        json_response = {
            'status': 'error',
            'message': message
        }
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)

#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) #?
def verify_email_verification_view(request):
    # if is_active = True 
    #   not do anything
    try:
        account = request.data.get('account')
        email = AccountModel.objects.get(account=account).email

        user_provided_verification_code = request.data.get('verification_code')

        stored_verification_code = get_stored_verification_code(email)
        
        if user_provided_verification_code == stored_verification_code:
            data = get_stored_signup_account(account)
            serializer = AccountSerializer(data=data)
            if not serializer.is_valid():
                json_response = {'status': 'error', 'message': serializer.errors}
                return Response(json_response, status=status.HTTP_404_NOT_FOUND)
            
            # = serializer def create(self, validated_data)
            user = serializer.save() # return object instance 
            user.set_password(user.password)
            user.is_active = True
            group = Group.objects.get(name='Engineers')
            group.uer_set.add(user)
            user.save()


            # user = AccountModel.objects.get(email=email)
            # user.is_active = True
            # user.save()
            

            delete_stored_verification_code(email)
            json_response = {'status': 'success', 'message': 'verification code successfully'}
            return Response(json_response, status=status.HTTP_200_OK)
        else:
            json_response = {'status': 'error', 'message': 'verification code error'}
            return Response(json_response, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        json_response = {
            'status': 'error',
            'message': message
        }
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)

#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login_view(request):
    account = request.data.get('account') # POST[''] # POST.get
    password = request.data.get('password')

    if count_limit('login_times', account, 3) == True:
        user = authenticate(request, account=account, password=password)
        if user is None:
            if AccountModel.objects.filter(account=account).exists(): 
                count = add_count_in_cache('login_times', account)
                json_response = {'status': 'error', 'message': 'error password', 'error times': count}
                return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    
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
    else:
        json_response = {'status': 'error', 'message': 'password error times over 3, login need to wait 5 mins'}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)

#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
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
    refresh_token = request.data.get('refresh_token')
    try: 
        token = RefreshToken(refresh_token)
        token.verify()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        json_response = {
            'status': 'error',
            'message': message
        }
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    payload = jwt.decode(refresh_token, secret_key='aaa', algorithms=['HS256'])

    json_response = {
        'status': 'success',
        'message': 'can get data',
    }
    return Response(json_response, status=status.HTTP_200_OK)

#-------------------------------------------------------------------------------#

# @api_view(['POST'])
# @csrf_exempt
# @permission_classes([AllowAny])
# def add_default_users_view(request): 
#     for i in range(1, 11):
#         data = {"account": f"user{i}", "email": f"user{i}@gmail.com", "name": f"user{i}", "password": "1234", "phone": "1234"}
#         serializer = AccountSerializer(data=data)
#         if not serializer.is_valid():
#             json_response = {'status': 'error', 'message': serializer.errors}
#             return Response(json_response, status=status.HTTP_404_NOT_FOUND)
#         user = serializer.save()
#         user.set_password(user.password)
#         user.is_active = True
#         user.save()
    
#     json_response = {
#         'status': 'success',
#         'message': 'default user1-10 created successfully (password=1234)',
#     }
#     return Response(json_response, status=status.HTTP_200_OK)

#-------------------------------------------------------------------------------#




# TODO
# if time not verification >rm data> use redis
# signup: rewrite email
# forget password
# delete: not active account 