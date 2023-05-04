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

from .jwt_utils import JWTUtils

# csrf
from django.views.decorators.csrf import csrf_exempt
# def generate_verification_code(length=6):
#     return ''.join([str(random.randint(0,9)) for _ in range(length)])

# def store_verification_code(email, code): # timeout=300
#     cache_key = f'verification_code_{email}'
#     cache.set(cache_key, code) # timeout

from django.contrib.auth.models import Group

import json

class CacheManager:
    def store_to_cache(stored_type: str, stored_id: str, stored_data: dict, stored_time: int, count=3): # time: sec
        cache_key = f'{stored_type}:{stored_id}'
        cache.set(cache_key, stored_data, stored_time)
    def delete_from_cache(stored_type: str, stored_id: str):
        cache_key = f'{stored_type}:{stored_id}'
        cache.delete(cache_key)
    def get_from_cache(stored_type: str, stored_id: str) -> int:
        cache_key = f'{stored_type}:{stored_id}'
        return cache.get(cache_key)
    def store_to_cache(stored_type: str, stored_id: str, stored_data: dict, stored_time: int):
        cache_key = f'{stored_type}:{stored_id}'
        cache.set(cache_key, stored_data, stored_time)

    def store_data_get_count(stored_type: str, stored_id: str, stored_data: dict, stored_time: int, count: int): # time: sec
        cache_key = f'{stored_type}:{stored_id}'
        if cache.get(cache_key): 
            stored_data = cache.get(cache_key)
            stored_count = stored_data['count']
            stored_count = stored_count+1
            if stored_count > count:
                return False
            else:
                stored_data['count'] = stored_count
                # cache.set(cache_key, stored_data, stored_time)
                # return stored_data
        else:
            stored_data['count'] = 1
            # cache.set(cache_key, stored_data, stored_time)
            # return stored_data

        # count not over
        if stored_type == 'signup_account':
            stored_data['verification_code'] =  send_email_verification_code(stored_data['account'], stored_data['email'])
            cache.set(cache_key, stored_data, stored_time)
        elif stored_type == 'login_account':
            stored_data['captcha'] , captcha_image_url = get_captcha_url()
            cache.set(cache_key, stored_data, stored_time)
        cache.get(cache_key, stored_data, stored_time)
        return  captcha_image_url# stored_data['count']

    def add_stored_data(stored_data, add_col, add_data):
        stored_data[add_col] = add_data



# def store_signup_account(json_data):
#     store_to_cache('signup_account', json_data['account'], json_data, 1) 
#     # print(json_data)
#     # account = json_data['account']
#     # cache_key = f'signup_account_{account}'
#     # cache.set(cache_key, json_data, 20)
    
# def get_stored_signup_account(account):
#     return get_from_cache('signup_account', account)
#     # cache_key = f'signup_account_{account}'
#     # json_data = cache.get(cache_key)    
#     # return json_data

# def get_stored_verification_code(email) :
#     get_from_cache('verification_code', email) 
#     # cache_key = f'verification_code_{email}'
#     # return cache.get(cache_key)

# def delete_stored_verification_code(email):
#     delete_from_cache('verification_code', email)
#     cache_key = f'verification_code_{email}'
#     cache.delete(cache_key)

# def send_email_verification_code(account, email):
#     # generate
#     verification_code = ''.join([str(random.randint(0,9)) for _ in range(6)])
#     # send
#     subject =  'T.A.P. verification code'
#     message = render_to_string('email_template.txt', {'account': account, 'verification_code': verification_code})
#     from_email = 's11a02d@gmail.com'
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list)
#     # store
#     cache_key = f'verification_code_{email}'
#     cache.set(cache_key, verification_code)

# def add_count_in_cache(type, item):
#     cache_key = f'{type}_{item}'
#     count = cache.get_or_set(cache_key, 0)
#     count += 1
#     cache.set(cache_key, count)
#     return count

# def count_limit(type, item, limit):
#     cache_key = f'{type}_{item}'
#     count = cache.get(cache_key)
#     if count is not None and count >= limit:
#         return False
#     return True

# #-------------------------------------------------------------------------------#


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



def get_stored_verification_code(email) :
    cache_key = f'verification_code_{email}'
    return json.loads(cache.get(cache_key))

def delete_stored_verification_code(email):
    cache_key = f'verification_code_{email}'
    cache.delete(cache_key)

def send_email_verification_code(account, email):
    """
    Generate verification code and send email to signup account.
    """
    verification_code = ''.join([str(random.randint(0,9)) for _ in range(6)])
    subject =  'T.A.P. verification code'
    message = render_to_string('email_template.txt', {'account': account, 'verification_code': verification_code})
    from_email = 's11a02d@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list) # slow 
    return verification_code




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
import captcha
# from captcha.helpers import captcha_image_url, random_char_challenge, reverse
# from captcha.urls import reverse

from .captcha_utils import get_captcha_url
logger = logging.getLogger(__name__)
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def test(request):
    # TODO
    # [] read account, password
    # [] read login count
    # captcha_value, captcha_iamge_url = get_captcha_url()
    account = 'user1'
    test = CacheManager.store_data_get_count(stored_type='login_account', stored_id=account, stored_data={}, stored_time=360, count=3)
    return JsonResponse({'captcha_value': test, 'captcha_iamge_url': 'captcha_iamge_url'})
    
  
    json_response = {
        'status': 'success',
        'message': 'signup & send email verification  successfully',
        'time': image
    }
    return Response(json_response, status=status.HTTP_200_OK)   


    # # 從 Redis 中獲取 captcha 值，如果不存在，則創建一個新的值
    # captcha_id = request.POST.get('captcha_id')
    # if captcha_id:
    #     captcha_value = r.get(captcha_id)
    # else:
    #     captcha_value = None

    # if not captcha_value:
    #     # 創建新的 captcha 值
    #     captcha_value = captcha.random_string(length=settings.CAPTCHA_LENGTH)

    #     # 將 captcha 值存儲到 Redis 中，並設置過期時間
    #     r.setex(captcha_value, settings.CAPTCHA_TIMEOUT, captcha_value)
    #     captcha_id = captcha_value

    # # 創建 captcha 圖片
    # image = captcha.create_image(captcha_value)
    # buf = io.BytesIO()
    # image.save(buf, 'png')
    # image_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    # image_url = f'data:image/png;base64,{image_str}'

    # # 返回 captcha 圖片的 URL 和 captcha_id
    # return JsonResponse({'image_url': image_url, 'captcha_id': captcha_id})


#-------------------------------------------------------------------------------#

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def signup_view(request):

    # TODO
    # user
    # [x] get data 
    # [x?] get serializer
    # [x] check sql ok? serializer to check
    # [] check cache exist? get 
  
    #   get=True count>3? wait min
    #   get=True count<3? count+1 
    #   get=False> count+1> varif 
    # [] check 

    serializer = AccountSerializer(data=request.data)
    
    # store_signup_account(serializer)
    if not serializer.is_valid(): # sql error
        json_response = {'status': 'error', 'message': serializer.errors}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    # user = serializer.save() # return object instance 
    # user.set_password(user.password)
    # user.is_active = False
    # group = Group.objects.get(name='Engineers')
    # group.uer_set.add(user)
    # user.save()

    # send_email_verification_code(serializer.data['account'], serializer.data['email'])

    count = CacheManager.store_data_get_count(stored_type='signup_account', stored_id=serializer.data['account'], stored_data=serializer.data, stored_time=360, count=3)

    json_response = {
        'status': 'success',
        'message': 'signup & send email verification  successfully',
        'account': serializer.data['account'],
        'time': count
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
        count = CacheManager.store_data_get_count(stored_type='signup_account', stored_id=account, stored_data=None, stored_time=60, count=3)
        json_response = {
            'status': 'success',
            'message': 'signup & send email verification  successfully',
            'account': account,
            'time': count
        }
        return Response(json_response, status=status.HTTP_200_OK)   

        
        # if count_limit('emailverification_times', account, 2) == True:
        #     count = add_count_in_cache('emailverification_times', account)
        #     send_email_verification_code(account, email)
        #     json_response = {
        #         'status': 'success',
        #         'message': 'resend email verification successfully',
        #         'error times': count
        #     }
        #     return Response(json_response, status=status.HTTP_200_OK)
        # else:
        #     json_response = {'status': 'error', 'message': 'send email times over 3, resend email need to wait 5 mins'}
        #     return Response(json_response, status=status.HTTP_404_NOT_FOUND)
        
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
    # try:
    account = request.data.get('account')
    user_provided_verification_code = request.data.get('verification_code')
    
    user_data = CacheManager.get_from_cache(stored_type='signup_account', stored_id=account)
    # return Response(user_data.pop ('verification_code', 'count'), status=status.HTTP_200_OK)
    stored_verification_code = user_data['verification_code']

    if user_provided_verification_code == stored_verification_code :
        # data = get_stored_signup_account(account)
        user_data.pop('verification_code')
        user_data.pop('count')
        serializer = AccountSerializer(data=user_data)

        if not serializer.is_valid():
            json_response = {'status': 'error', 'message': serializer.errors}
            return Response(json_response, status=status.HTTP_404_NOT_FOUND)
        
        # = serializer def create(self, validated_data)
        user = serializer.save() # return object instance 
        user.set_password(user.password)
        user.is_active = True
        group = Group.objects.get(name='Engineers')
        group.user_set.add(user)
        user.save()


        # user = AccountModel.objects.get(email=email)
        # user.is_active = True
        # user.save()
        
        CacheManager.delete_from_cache(stored_type='signup_account', stored_id=serializer.data['account'])
        json_response = {'status': 'success', 'message': 'create'}
        return Response(json_response, status=status.HTTP_200_OK)
    else:
        json_response = {'status': 'error', 'message': 'verification code error'}
        return Response(json_response, status=status.HTTP_404_NOT_FOUND)
    
    # except Exception as ex:
    #     template = "An exception of type {0} occurred. Arguments:{1!r}"
    #     message = template.format(type(ex).__name__, ex.args)
    #     json_response = {
    #         'status': 'error',
    #         'message': message
    #     }
    #     return Response(json_response, status=status.HTTP_404_NOT_FOUND)

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
        
        jwt_token = JWTUtils.create_jwt(user.id, user_role='engineer', data=None)
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
# @authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
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
# @authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def jwt_view(request):
    payload = JWTUtils.verify_jwt(request)

    json_response = {
        'status': 'success',
        'message': payload
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




# TODO
# if time not verification >rm data> use redis
# signup: rewrite email
# forget password
# delete: not active account 