import os
from settings._base import *

DEBUG = True

STATIC_ROOT = (os.path.join(BASE_DIR, 'compiled_static'))
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Allow all host headers
ALLOWED_HOSTS = ['*']
