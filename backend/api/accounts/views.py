
from api.accounts.models import AccountModel
from api.accounts.serializers import AccountSerializer
from rest_framework import viewsets

from django.conf import settings
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token

# session
# from django.contrib.auth import authenticate, login, logout
# jwt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
# simplejwt
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin 
# simplejwt_login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group


from api.accounts.captcha_utils import CaptchaManager

from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache


import logging
import traceback
logger = logging.getLogger(__name__)

SIGNUP_TIME_INTERVAL = 120

#-------------------------------------------------------------------------------#
# TODO
# forget password
# delete: not active account 
# response setting cookie 
# 記住我


from rest_framework import permissions


class AccountPermission(permissions.BasePermission): 
    def has_permission(sekf, request, view):
        if request.user and request.user.is_authenticated:
            group_manager = Group.objects.get(name='Managers')
            if not group_manager in request.user.groups.all():
                if view.action == 'retrieve':
                    return True

            elif group_manager in request.user.groups.all():
                if request.method == 'GET' or request.method == 'DELETE':
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        group_manager = Group.objects.get(name='Managers')
        if not group_manager in request.user.groups.all():
            if view.action == 'retrieve' and request.user == obj:
                return True
            
        elif group_manager in request.user.groups.all():
            if request.method == 'GET' or request.method == 'DELETE':
                return True 
        return False



from rest_framework import mixins
@permission_classes([AccountPermission])
class AccountViewSet(viewsets.ModelViewSet):
   queryset = AccountModel.objects.all()
   serializer_class = AccountSerializer
   

#-------------------------------------------------------------------------------#


class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['account'] = user.account
        if user.groups.filter(name='Managers').exists():
            token['group'] = 'manager'
        else:
            token['group'] = 'engineer'
        return token






#-------------------------------------------------------------------------------#
# captcha
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def generate_captcha_view(request):
    try:
        # create new captcha and store to cache
        image_url = CaptchaManager.generate_captcha() 
        return Response({'status':'success', 'image_url': image_url}, status=status.HTTP_200_OK)
    except:
        return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def verify_captcha_view(request):
    try:
        image_url = request.data.get('image_url')
        captcha_value = request.data.get('captcha_value')
        if CaptchaManager.verify_captcha(captcha_value, image_url):
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
#-------------------------------------------------------------------------------#
# login, logout
class PostStatusMixin:
    def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                response.data['sataus'] = 'success'
            elif response.status_code == 401:  
                response.data['sataus'] = 'error_me'
            return response

# @api_view(['POST'])
# @csrf_exempt
# @permission_classes([AllowAny])
class LoginTokenView(PostStatusMixin, TokenObtainPairView):
    serializer_class = LoginTokenSerializer


class LogoutTokenView(PostStatusMixin, TokenBlacklistView):
    pass


class RefreshTokenView(PostStatusMixin, TokenRefreshView):
    pass


#-------------------------------------------------------------------------------#
# signup

from rest_framework import permissions
class GroupPermission(permissions.BasePermission): 
    """
        
    """
    def has_permission(self, request, view):
        # return request.user.groups.filter(name='Managers').exists()
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.user and request.user.is_authenticated:
            group_manager = Group.objects.get(name='Managers')
            if group_manager in request.user.groups.all():
                return True   
            else:
                return False
        return False
    
@api_view(['POST'])
@csrf_exempt
@permission_classes([GroupPermission])
# @authentication_classes([JWTAuthentication])
def temp_store_signup_data_view(request):
    try:
        serializer = AccountSerializer(data=request.data) 
        if serializer.is_valid():
            account = serializer.data['account']
            cache.set(f'signup_user:{account}', serializer.data, SIGNUP_TIME_INTERVAL)
            # user_id, account, group
            return Response({'status': 'success', 'signup_account': account}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'signup invalid'}, status=status.HTTP_404_NOT_FOUND)
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
        return Response(json_data)

from .email_verification_utils import send_email_verification_code
@api_view(['POST'])
@csrf_exempt
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@permission_classes([GroupPermission])
# @authentication_classes([JWTAuthentication])
def send_email_verification_code_view(request):
    try:
        account = request.data.get('account')
        if cache.get(f'signup_user:{account}'):
            user = cache.get(f'signup_user:{account}')
            email = user['email']
            verification_code = send_email_verification_code(account, email)
            cache.set(f'signup_user:verification_code:{account}', verification_code, SIGNUP_TIME_INTERVAL)
            return Response({'status': 'success', 'signup_account': account, 'verification_code': verification_code}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
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
        return Response(json_data)
    
@api_view(['POST'])
@csrf_exempt
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@permission_classes([GroupPermission])
# @authentication_classes([JWTAuthentication])
def verify_email_verification_code_view(request):
    account = request.data.get('account')
    provided_verification_code = request.data.get('verification_code')
    if provided_verification_code == cache.get(f'signup_user:verification_code:{account}'):
        serializer_data = cache.get(f'signup_user:{account}')
        serializer = AccountSerializer(data=serializer_data)
        if serializer.is_valid():
            user = serializer.save()
            user.approver = request.user.id
            user.set_password(user.password)
            user.is_active = True
            group = Group.objects.get(name='Engineers')
            group.user_set.add(user)
            user.save()
            return Response({'status': 'success', 'signup_account': account}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'signup invalid (timeout)'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'status': 'error', 'message': 'email verification invalid'}, status=status.HTTP_404_NOT_FOUND)

