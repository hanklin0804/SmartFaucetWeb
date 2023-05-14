from django.urls import path
from api.accounts import views
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenVerifyView, TokenRefreshView

from django.urls import include
from rest_framework import routers
router = routers.DefaultRouter()
router.register('', views.AccountViewSet)


urlpatterns = [
    path('rest/', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    # path('defaultusers/', views.add_default_users_view, name='defaultusers'),
    path('verify.email/', views.verify_email_verification_view, name='verify.email'),
    path('resend.email/', views.resend_email_verification_view, name='resend.email'),
    path('account.info/', views.account_information_view, name='account.info'),

    path('jwt/', views.jwt_view, name='jwt'),

    # path('test/', views.test, name='test'),
    path('generate.captcha/', views.generate_captcha_view, name='generate.captcha'),
    path('verify.captcha/', views.verify_captcha_view, name='verify.captcha'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
