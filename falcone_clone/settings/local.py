# falcone_clone/settings/local.py
from .base import *
from decouple import config

# Local development settings
DEBUG = config('DEBUG', default=True, cast=bool)
ENV = config('ENVIRONMENT', default='development')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
