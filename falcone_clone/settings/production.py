from .base import *

DEBUG = False
ALLOWED_HOSTS = ['falconoptics.com.ua',
                 'www.falconoptics.com.ua', 'vps71960.hyperhost.name']

# продакшен-орієнтоване сховище медіа
MEDIA_ROOT = '/var/www/media/'

# безпечні cookie + HTTPS редирект
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
