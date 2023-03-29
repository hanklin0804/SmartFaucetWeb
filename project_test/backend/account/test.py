import jwt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from .models import CustomUser

# 生成 JWT Token 的函數
def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    }

    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    return token

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)

        # 驗證 reCAPTCHA，請確保在前端已實作 reCAPTCHA
        recaptcha_response = request.data.get('recaptcha_response')
        if not validate_recaptcha(recaptcha_response):
            return Response({'status': 'error', 'message': 'reCAPTCHA 驗證失敗'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()

            jwt_token = generate_jwt_token(user)

            return Response({
                'status': 'success',
                'message': '註冊成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'jwt_token': jwt_token
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
                'status': 'error',
                'message': '註冊失敗',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': 'error', 'message': '不支持的請求方法'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    




    @api_view(['POST'])
def login_view(request):
    recaptcha_token = request.data.get('recaptcha_token') # POST.get
    if not verify_recaptcha(recaptcha_token):
        return Response()
        # permission_classes = [permissions.AllowAny]
        # get data
        account = request.data.get('account') # POST['']
        password = request.data.get('password')
        user = authenticate(request, account=account, password=password)
        if user is not None:
            # login
            login(request, user)
            # generate simpletoken
            jwt_token = {
                'access_token': str(AccessToken.for_user(user)),
                'refresh_token': str(RefreshToken.for_user(user)),
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

            # create token
            # token, created = Token.objects.get_or_create(user=user)
            # json_data = {'token': token.key}
            return Response(json_response, status=status.HTTP_200_OK)
        json_response = {'status': 'failure', 'error': 'Invalid username or password'}
        return Response(json_response, status=status.HTTP_400_BAD_REQUEST)
    json_response = {'status': 'failure', 'error': 'reCAPTHCHA verification failed'}
    return Response(json_response, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register_view(request): 
    recaptcha_token = request.data.get('recaptcha_token')
    if verify_recaptcha(recaptcha_token):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            # = serializer def create(self, validated_data)
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            # return JsonResponse({"status": "success"})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse({"status": "failed", "error": "Invalid username or password"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return JsonResponse({"status": "failed", "error": "reCAPTCHA verification failed"})
    return Response({'detail': 'reCAPTCHA verification failed'}, status=status.HTTP_401_UNAUTHORIZED)
