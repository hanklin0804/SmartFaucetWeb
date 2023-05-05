from django.urls import path
from api.accounts import views

urlpatterns = [
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
    path('verify.captcha/', views.verify_captcha_view, name='verify.captcha')
]
