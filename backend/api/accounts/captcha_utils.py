import json
import logging


import io
import base64

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import captcha
import redis
from PIL import Image

from django.conf import settings
from captcha.image import ImageCaptcha
import captcha



def get_captcha_url():

    # captcha_value = captcha.rnadom_string(length=10)
    value = 'test'
    image = ImageCaptcha(width=settings.CAPTCHA_IMAGE_SIZE[0], height=settings.CAPTCHA_IMAGE_SIZE[1])
    # image.write('test', ('test')+'.png')
    image_data = image.generate(value)
    image_str = base64.b64encode(image_data.getvalue()).decode('utf-8')
    image_url = f'data:image/png;base64,{image_str}'

    return value, image_url
 


# from captcha.helpers import captcha_image_url, random_char_challenge, reverse

# def get_captcha_url():

#     new_key = random_char_challenge()
#     image_url = captcha_image_url(new_key) # error
  
#     return image_url