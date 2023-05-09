from django.core.cache import cache
from .email_verification_utils import send_email_verification_code

class AccountWorkManager:
    def account_work(stored_type: str, stored_id: str, stored_data: dict, stored_time: int, count_limit: int, verification_code=None): # time: sec
        cache_key = f'{stored_type}:{stored_id}'
        if cache.get(cache_key): 
            stored_data = cache.get(cache_key)
            stored_count = stored_data['count']
            stored_count = stored_count+1
            if stored_count > count_limit:
                return False
            else:
                stored_data['count']  = stored_count
        else:
            stored_data['count']  = 1

        # do 
        if stored_type == 'signup_account':
            stored_data['verification_code'] =  send_email_verification_code(stored_data['account'], stored_data['email'])
        if stored_type == 'verify_signup':
            stored_verification_code = cache.get(f'signup_account:{stored_id}')['verification_code']
            if stored_verification_code != verification_code:
                return False
        
        cache.set(cache_key, stored_data, stored_time) 
        return True # stored_data['count'] 
    

    def add_stored_data(stored_data, add_col, add_data):
        stored_data[add_col] = add_data



