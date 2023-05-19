from django.urls import path
from api.accounts import views
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenVerifyView, TokenRefreshView

from django.urls import include
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'management', views.AccountViewSet)
# port forwarding

urlpatterns = [    
    path('', include(router.urls)),
    # path('test/', views.test, name='test'),

 
    path('auth/login/', views.LoginTokenView.as_view(), name='login'),
    path('auth/logout/', views.LogoutTokenView.as_view(), name='logout'),
    path('auth/refresh/', views.RefreshTokenView.as_view(), name='token_refresh'),
    # path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('signup/data/', views.temp_store_signup_data_view, name='signup'),
    path('signup/email/send/', views.send_email_verification_code_view, name='signup-email-send'),
    path('signup/email/verify/', views.verify_email_verification_code_view, name='signup-email-verify'),


    path('captcha/generate/', views.generate_captcha_view, name='generate_captcha'),
    path('captcha/verify/', views.verify_captcha_view, name='verify_captcha'),
    

]
