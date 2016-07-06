import os
from _base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': '0WUX5AwY6x',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
) #specifies all the folders on your system where Django should look for static files

STATIC_ROOT = (os.path.join(BASE_DIR, 'compiled_static'))
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Allow all host headers
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
