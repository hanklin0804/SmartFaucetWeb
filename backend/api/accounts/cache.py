from django.core.cache import cache

class AccountCache():
    def store_user_data(json_data):
        print(json_data)
        account = json_data['account']
        cache_key = f'signup_account_{account}'
        cache.set(cache_key, json_data, 20)
    
    def get_user_data(account):
        cache_key = f'signup_account_{account}'
        json_data = cache.get(cache_key)    
        return json_data




    def get_stored_verification_code(email) :
        cache_key = f'verification_code_{email}'
        return cache.get(cache_key)

def delete_stored_verification_code(email):
    cache_key = f'verification_code_{email}'
    cache.delete(cache_key)

def send_email_verification_code(account, email):
    # generate
    verification_code = ''.join([str(random.randint(0,9)) for _ in range(6)])
    # send
    subject =  'T.A.P. verification code'
    message = render_to_string('email_template.txt', {'account': account, 'verification_code': verification_code})
    from_email = 's11a02d@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    # store
    cache_key = f'verification_code_{email}'
    cache.set(cache_key, verification_code)

def add_count_in_cache(type, item):
    cache_key = f'{type}_{item}'
    count = cache.get_or_set(cache_key, 0)
    count += 1
    cache.set(cache_key, count)
    return count

def count_limit(type, item, limit):
    cache_key = f'{type}_{item}'
    count = cache.get(cache_key)
    if count is not None and count >= limit:
        return False
    return True

