from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    # path('register/',views.register_view, name='register'), 
    # path('account/', views.account_view, name= 'account'),
    # path('account/faucet/setting/', views.device_setting_view),
    # path('account/faucet/information', views.device_instant_info),
]