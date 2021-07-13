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

DEBUG = True

STORAGE_DIR = Path('storage')
