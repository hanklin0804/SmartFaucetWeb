import jwt

from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt():
    dt = datetime.now()+timedelta(days=60)

    header = {
        "userId": "abcd123",
        "expiry": 1646635611301
    }
    payload = {

        "iss": "https://accounts.google.com",
        "azp": "1234987819200.apps.googleusercontent.com",
        "aud": "1234987819200.apps.googleusercontent.com",
        "sub": "10769150350006150715113082367",
        "at_hash": "HK6E_P6Dh8Y93mRNtsDB1Q",
        "email": "jsmith@example.com",
        "email_verified": "true",
        "iat": 1353601026,
        "exp": 1353604926,
        "nonce": "0394852-3190485-2490358",
        "hd": "example.com"

    }
    # Bease64URLSafe(
    #     HMACSHA256((<header>, <payload>, <secret key>))
    # )
    
    # jwt.encode(payload={}, settings.SECRET_KEY, algotithm='HS256')
    encoded_jwt = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    print(encoded_jwt)

def check_jwt(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
    
    token = auth_header[1]
    try:
        # jwt.decode(encoded_jwt, 'secret', algorithms=['hs256'])
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHMS])
    except:
        pass 
        return 


generate_jwt()

