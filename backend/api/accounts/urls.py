from django.urls import path
from api.accounts import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('defaultusers/', views.add_default_users_view, name='defaultusers'),
]