import jwt
import datetime
from django.conf import settings

ROLE_PERMISSIONS = {
    'engineer': ['read', 'write'],
    'manager': ['read', 'write']
}


class JWTUtils:
    def create_jwt(user_id, user_role, data=None):
        now = datetime.datetime.utcnow() #tz=None 
        payload = {
            # user_id, role, permissions
            'user_id': user_id,
            'iat': now,
            'exp': now + datetime.timedelta(minutes=5),
            'role': user_role,
            # 'jti': set(user_id) + set(now.timestamp()), # jwt id/uid
        }
        token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        return token

    # def check_jwt(request):
    #     auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
    
    #     token = auth_header[1]
    def verify_jwt(token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
            return payload, None
        except jwt.ExpiredSignatureError as ex:
            print('Token expired.')
            return None, ex
        except jwt.InvalidTokenError as ex:
            print('Invalid token.')
            return None, ex
        
    # user_permissions = ROLE_PERMISSIONS.get(user_role, [])     



# print("Encoded JWT:", jwt_string)
# print("Decoded Payload:", decoded_payload)
