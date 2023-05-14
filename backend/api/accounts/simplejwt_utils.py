from rest_framework_simplejwt.tokens import RefreshToken


def generate_simplejwt(user):
    refresh = RefreshToken.for_user(user)
    json_data = {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }
    return json_data


def black_simplejwt(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        # token.check_blacklist()
        return 1
    except:
        return 0

