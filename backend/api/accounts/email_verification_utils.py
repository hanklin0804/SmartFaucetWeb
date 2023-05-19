from django.template.loader import render_to_string
from django.core.mail import send_mail
from .random_utils import RandomGenerateString

# TODO: create new thread
def send_email_verification_code(account, email):
    """
    Generate verification code and send email to signup account.
    """
    verification_code = RandomGenerateString.generate_numbers(len=5)
    subject =  'T.A.P. verification code'
    message = render_to_string('email_template.txt', {'account': account, 'verification_code': verification_code})
    from_email = 's11a02d@gmail.com'
    recipient_list = [email]
    # TODO: dead
    # send_mail(subject, message, from_email, recipient_list) # slow 
    return verification_code
