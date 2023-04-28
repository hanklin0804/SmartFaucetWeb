import jwt
import datetime
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

ROLE_PERMISSIONS = {
    'engineer': ['read', 'write'],
    'manager': ['read', 'write', 'manager']
}


class JWTUtils:
    def create_jwt(user_id, user_role, data=None):
        now = datetime.datetime.utcnow() #tz=None 
        payload = {
            # user_id, role, permissions
            'user_id': user_id,
            'iat': now,
            'exp': now + datetime.timedelta(minutes=1),
            'role': user_role,
            # 'jti': set(user_id) + set(now.timestamp()), # jwt id/uid
        }
        token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        return token

    # def check_jwt(request):
    #     auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
    
    #     token = auth_header[1]
    def verify_jwt(request):
        try:
            token = request.data.get('token')
            payload = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
            return payload, None
        
        except jwt.ExpiredSignatureError:
            json_response = {
                'status': 'error',
                'message': 'Token expired.'
            }
            return None, json_response
        except jwt.InvalidTokenError:
            json_response = {
                'status': 'error',
                'message': 'Invalid token.'
            }
            return None, json_response

        
        
    # user_permissions = ROLE_PERMISSIONS.get(user_role, [])     



# print("Encoded JWT:", jwt_string)
# print("Decoded Payload:", decoded_payload)
