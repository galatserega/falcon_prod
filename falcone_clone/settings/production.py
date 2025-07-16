from .base import *
from decouple import config

# Production-specific settings
DEBUG = config('DEBUG', default=False, cast=bool)
ENV = config('ENVIRONMENT', default='production')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='falconoptics.com.ua,www.falconoptics.com.ua,vps71960.hyperhost.name', cast=lambda v: [s.strip() for s in v.split(',')])

# Production-oriented media storage
MEDIA_ROOT = '/var/www/media/'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
