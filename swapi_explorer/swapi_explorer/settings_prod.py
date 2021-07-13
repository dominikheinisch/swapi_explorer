from .settings import *
from pathlib import Path


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'PASSWORD': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
    }
}

DEBUG = False

ALLOWED_HOSTS = ['*']

STORAGE_DIR = Path('storage')
