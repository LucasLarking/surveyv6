from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-vs0c653wn%=6$w(!pjlon^(x14)ln5g)ysv8q-&@uw@fcc)=^)'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}