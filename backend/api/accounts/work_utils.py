from django.core.cache import cache
from .email_verification_utils import send_email_verification_code

from django.contrib.auth import authenticate, login, logout
from api.accounts.models import AccountModel

from .serializers import AccountSerializer
from django.contrib.auth.models import Group


def login_work(request) -> dict:
    user = authenticate(account=request.data.get('account'), password=request.data.get('password'))
    if user:
        login(request, user)
        return True
        # json_data = {'status': 'success'}
    else:
        return False
    #     # error
    #     if AccountModel.objects.filter(account=request.data.get('account')).exists():
    #         # password error
    #         json_data = {'status': 'error'} #, 'message': 'password'}
    #     else:
    #         # other error
    #         json_data = {'status': 'error'} #, 'message': 'empty or not exist'}
    # return json_data # user


def verify_user(account, verification_code):
    user_data = cache.get(f'signup_account:{account}')
    if  user_data['verification_code'] == verification_code:
        user_data.pop('verification_code')
        user_data.pop('count')
        return user_data
    else:
        return False


def signup_work(user_data):   
    serializer = AccountSerializer(data=user_data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(user.password)
        user.is_active = True
        group = Group.objects.get(name='Engineers')
        group.user_set.add(user)
        user.save()
        json_response = {'status': 'success'}
        return json_response
    else:
        json_response = {'status': 'error'}
        return json_response


class WorkManager:
    def account_work(type: str, account: str, stored_time: int, times_limit: int, stored_data={}, data=None): # time: sec
        # check times
        # do
        # success > not update times
        # error > updata times
             
        cache_key = f'{type}:{account}'
        if cache.get(cache_key): 
            stored_data = cache.get(cache_key)
            stored_count = stored_data['count']
            stored_count = stored_count+1
            if stored_count > times_limit:
                return False
            else:
                stored_data['count']  = stored_count
        else:
            stored_data['count']  = 1
            
        if type == 'login' and login_work(data):
            json_response = {'status': 'success'}
            return json_response

        if type == 'verify_signup' and (user_data:=verify_user(account, data)) and signup_work(user_data):
            json_response = {'status': 'success'}
            return json_response
        
        if type == 'signup_userdata':
            stored_data['verification_code'] =  send_email_verification_code(stored_data['account'], stored_data['email'])
            cache.set(cache_key, stored_data, stored_time) 
            json_response = {'status': 'success'}
            return json_response
        

        # +1
        cache.set(cache_key, stored_data, stored_time) 
        return {'status': 'error'} # stored_data['count'] 
    





