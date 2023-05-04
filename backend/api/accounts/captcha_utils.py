from django.conf import settings
from captcha.image import ImageCaptcha
import base64
from .cache_utils import CacheManager
from .random_utils import RandomGenerateString
# import io
# from PIL import Image


class CaptchaManager():
    def generate_captcha() -> str:
        captcha_value = RandomGenerateString.generate_string(5)
        image = ImageCaptcha(width=settings.CAPTCHA_IMAGE_SIZE[0], height=settings.CAPTCHA_IMAGE_SIZE[1])
        # image.write('test', ('test')+'.png')
        image_data = image.generate(captcha_value)
        image_str = base64.b64encode(image_data.getvalue()).decode('utf-8')
        image_url = f'data:image/png;base64,{image_str}'
        CacheManager.store_to_cache(stored_type='captcha', stored_id=image_url, stored_data=captcha_value.lower(), stored_time=500)
        return image_url
    
    def verify_captcha(user_provided_captcha_value: str, image_url: str) -> bool:
        captcha_value = CacheManager.get_from_cache(stored_type='captcha', stored_id=image_url)
        
        if user_provided_captcha_value.lower() == captcha_value:
            CacheManager.delete_from_cache(stored_type='captcha', stored_id=image_url)
            return True
        else:
            return False
        


   # captcha_id = request.POST.get('captcha_id')
    # if captcha_id:
    #     captcha_value = cache.get(captcha_id)
    # else:
    #     captcha_value = None

    # if not captcha_value:
    #     # 創建新的 captcha 值
    #     captcha = CaptchaStore.generate()
    #     captcha_value = captcha.hashkey

    #     # 將 captcha 值存儲到 Redis 中，並設置過期時間
    #     cache.set(captcha_value, captcha, settings.CAPTCHA_TIMEOUT)
    #     captcha_id = captcha_value

    # # 創建 captcha 圖片
    # image = captcha_image(request, captcha_value)
    # buf = io.BytesIO()
    # image.save(buf, 'png')
    # image_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    # image_url = f'data:image/png;base64,{image_str}'

    # # 返回 captcha 圖片的 URL 和 captcha_id
    # return HttpResponse(
    #     json.dumps({'image_url': image_url, 'captcha_id': captcha_id}),
    #     content_type='application/json'
    # )
  