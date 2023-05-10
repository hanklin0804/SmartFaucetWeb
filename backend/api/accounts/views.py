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



# csrf
from django.views.decorators.csrf import csrf_exempt
# def generate_verification_code(length=6):
#     return ''.join([str(random.randint(0,9)) for _ in range(length)])

# def store_verification_code(email, code): # timeout=300
#     cache_key = f'verification_code_{email}'
#     cache.set(cache_key, code) # timeout

from django.contrib.auth.models import Group

import json

from .jwt_utils import JWTUtils
from .captcha_utils import CaptchaManager
from .cache_utils import CacheManager


#-------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------#
import json
import logging


import io
import base64

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import captcha
import redis
from PIL import Image

from django.conf import settings



from captcha.image import ImageCaptcha
# from captcha.helpers import captcha_image_url, random_char_challenge, reverse
# from captcha.urls import reverse

# from .captcha_utils import generate_captcha

from django_ratelimit.decorators import ratelimit


from .work_utils import WorkManager

logger = logging.getLogger(__name__)

import traceback


# from ratelimit import limits
# @limits(calls=5, period=60)
# @ratelimit(key='ip', rate='2/m', method='POST', block=True)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def sample_view(request):
    try:
        # code
        pass
    except Exception as ex:
        current_frame = traceback.extract_tb(ex.__traceback__)
        file_name, line_number, function_name, text = current_frame[-1]

        json_data = {
            'File:': file_name,
            'Line:': line_number,
            'Function:': function_name,
            'Text:': text,
            'Error':
            {
                'error_class': ex.__class__.__name__,
                'error_message:': ex.args 
            }           
        }
        return JsonResponse(json_data)
    
    # except Exception as ex:
    #     template = "An exception of type {0} occurred. Arguments:{1!r}"
    #     message = template.format(type(ex).__name__, ex.args)
    #     json_response = {
    #         'status': 'error',
    #         'message': message
    #     }
    #     return Response(json_response, status=status.HTTP_404_NOT_FOUND)


#-------------------------------------------------------------------------------#
# ok
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def generate_captcha_view(request):
    try:
        # create new captcha and store to cache
        image_url = CaptchaManager.generate_captcha() 
        return JsonResponse({'status':'success', 'iamge_url': image_url}, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def verify_captcha_view(request):
    try:
        image_url = request.data.get('image_url')
        captcha_value = request.data.get('captcha_value')
        if CaptchaManager.verify_captcha(captcha_value, image_url):
            return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return JsonResponse({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
#-------------------------------------------------------------------------------#
# ok
# TODO
# [x] get account, password
# [x] check times
# [x] check user
# [] get user data
# [] generate jwt

from .simplejwt_utils import block_simplejwt, generate_simplejwt

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login_view(request):
    account = request.data.get('account')
    password = request.data.get('password')
    json_data = WorkManager.account_work(type='login', 
                                         account=account, 
                                         data=request,
                                         stored_time=300, 
                                         times_limit=3) 
    if json_data: 
        user = authenticate(request, account=account, password=password)
        json_data.update(generate_simplejwt(user))
        return JsonResponse(json_data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
  
#-------------------------------------------------------------------------------#
# 
# TODO
# [x] get data 
# [x] get serializer
# [x] check sql > serializer
# [x] check times & cache
# [x] send email

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def signup_view(request):
    serializer = AccountSerializer(data=request.data) 
    if serializer.is_valid():
        # not store to sql
        # check cache 
        json_data = WorkManager.account_work(type='signup_userdata', 
                                             account=serializer.data['account'], 
                                             stored_data=serializer.data, 
                                             stored_time=300, 
                                             times_limit=1)
        if json_data:
            return Response({'status': 'success'}, status=status.HTTP_200_OK) 
        else:
            return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)  
    else:
        return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)  

#-------------------------------------------------------------------------------#
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) #?
def resend_email_verification_view(request):
    try:
        account = request.data.get('account')
        json_data = WorkManager.account_work(type='signup_userdata', 
                                             account=account, 
                                             stored_time=300, 
                                             times_limit=3)
        if json_data:
            return Response(json_data, status=status.HTTP_200_OK)   
        else:
            return Response({'status': 'error_count'}, status=status.HTTP_404_NOT_FOUND)  
    except:
        return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)  


#-------------------------------------------------------------------------------#
# TODO
# [] count
# [] verify
# [] signup setting & save
# [] setting & save
# [] delete? 

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) #?
def verify_email_verification_view(request):
    account = request.data.get('account')
    user_provided_verification_code = request.data.get('verification_code')
    json_data = WorkManager.account_work(type='verify_signup', 
                                         account=account, 
                                         data=user_provided_verification_code,
                                         stored_time=300, 
                                         times_limit=3
                                         )
    if json_data:
        return Response(json_data, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
    
    # except Exception as ex:
    #     template = "An exception of type {0} occurred. Arguments:{1!r}"
    #     message = template.format(type(ex).__name__, ex.args)
    #     json_response = {
    #         'status': 'error',
    #         'message': message
    #     }
    #     return Response(json_response, status=status.HTTP_404_NOT_FOUND)


#-------------------------------------------------------------------------------#
# TODO 
# [] logout
# [] jwt 
@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def logout_view(request):
  
    # # jwt: delete
    # token = request.data.get('token')
    # # token = RefreshToken(token)
    # token.blacklist()

    logout(request) # clean auth session data

    json_response = {'status': 'success'}
    return Response(json_response, status=status.HTTP_200_OK)


#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def jwt_view(request):
    # payload = JWTUtils.verify_jwt(request)
    # refresh_token = request.data.get('refresh_token')

    # token = RefreshToken(refresh_token)
    # token.verify()
    json_response = {
        'status': 'success',
        'message': 'ok'
    }
    return Response(json_response, status=status.HTTP_200_OK)
   

#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def account_information_view(request):
    payload, json_response = JWTUtils.verify_jwt(request)
    if payload:
        json_response = {
            'status': 'success',
            'message': payload['user_id']
        }
        return Response(json_response, status=status.HTTP_200_OK)
    else:
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)

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


def session(request):
    request.session['key'] = 'key'
    request.session.get('key', 'default_value')

    return Response()

request.session.save()

# TODO
# if time not verification >rm data> use redis
# signup: rewrite email
# forget password
# delete: not active account 


def get_cookie(request):
    if 'cookie' in request.COOKIES:
        json_data = {
            'cookie': request.COOKIES['cookie']
        }
        return Response(json_data)
    return Response({'status': 'error'})


def get_cookie(request):
    if 'cookie' in request.COOKIES:
        json_data = {
            'cookie': request.COOKIES['cookie']
        }
        return Response(json_data)
    return Response({'status': 'error'})