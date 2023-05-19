from rest_framework_simplejwt.tokens import RefreshToken


def generate_simplejwt(user):
    refresh = RefreshToken.for_user(user)
    json_data = {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }
    return json_data


def black_simplejwt(refresh_token): 
    token = RefreshToken(refresh_token)
    token.blacklist()
       

