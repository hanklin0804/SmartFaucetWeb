from django.core.cache import cache
from .email_verification_utils import send_email_verification_code

class CacheManager:
    def store_to_cache(stored_type: str, stored_id: str, stored_data: dict, stored_time: int): # time: sec
        cache_key = f'{stored_type}:{stored_id}'
        cache.set(cache_key, stored_data, stored_time)
    def delete_from_cache(stored_type: str, stored_id: str):
        cache_key = f'{stored_type}:{stored_id}'
        cache.delete(cache_key)
    def get_from_cache(stored_type: str, stored_id: str) -> int:
        cache_key = f'{stored_type}:{stored_id}'
        return cache.get(cache_key)
    def store_to_cache(stored_type: str, stored_id: str, stored_data: dict, stored_time: int):
        cache_key = f'{stored_type}:{stored_id}'
        cache.set(cache_key, stored_data, stored_time)

    def store_data_get_count(stored_type: str, stored_id: str, stored_data: dict, stored_time: int, count: int): # time: sec
        cache_key = f'{stored_type}:{stored_id}'
        if cache.get(cache_key): 
            stored_data = cache.get(cache_key)
            stored_count = stored_data['count']
            stored_count = stored_count+1
            if stored_count > count:
                return False
            else:
                stored_data['count'] = stored_count
                # cache.set(cache_key, stored_data, stored_time)
                # return stored_data
        else:
            stored_data['count'] = 1
            # cache.set(cache_key, stored_data, stored_time)
            # return stored_data

        # do 
        if stored_type == 'signup_account':
            stored_data['verification_code'] =  send_email_verification_code(stored_data['account'], stored_data['email'])
        cache.set(cache_key, stored_data, stored_time) 
        return stored_data['count'] 

    def add_stored_data(stored_data, add_col, add_data):
        stored_data[add_col] = add_data



# CacheManager.store_data_get_count(stored_type='login_account', stored_id=account, stored_data={}, stored_time=360, count=3)