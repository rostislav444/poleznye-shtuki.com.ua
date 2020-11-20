import os
from .local_settings import *
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILE_DIR  = os.path.join(BASE_DIR, 'static')

SECRET_KEY = "very_secret_key_123"

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','185.233.119.159','poleznye-shtuki.com.ua','www.poleznye-shtuki.com.ua']


APPEND_SLASH = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # APPS
    'apps.core.apps.CoreConfig',
    'apps.shop',
    'apps.cart',
    'apps.order',
    'apps.user',
    'apps.comments',
    'apps.search',
    'apps.seo',
    'apps.pages',
    # MODULES
    'mptt',
    'compressor',
    'ckeditor',
    'colorfield',
    'easy_select2',
    'rest_framework',
    'clear_cache',
]





MIDDLEWARE = [
    'django.middleware.http.ConditionalGetMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # CAHCHE
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.context_processors.languages',
                'apps.shop.context_processors.categories',
                'apps.cart.context_processors.cart',
            ],
            'libraries': {}
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

GEOIP_PATH =  os.path.join(BASE_DIR, 'project/geo/GeoLite2-Country.mmdb')

DROP1_API_TOKEN = 'grPZ0FA2iYHHeKx0FG897jnuZc7VXMMoC3WmgEmOn6tcU16TcyBoCwe7bSCP'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTHENTICATION_BACKENDS = [
    'project.auth.UserAuthentication',
]
AUTH_USER_MODEL = 'user.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('ru', 'Russian'),
    ('uk', 'Ukrainian'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# LANGUAGES = [{ language.code : language.name } for language in Languages.objects.all()]


# STATIC
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
STATICFILES_DIRS = [
    STATICFILE_DIR,
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_URL
# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# E-MAIL
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD='streetride24'
EMAIL_HOST_USER='rostislav444@gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# CART
CART_SESSION_ID = 'cart'
# WISHLIST
WISHLIST_SESSION_ID = 'wishlist'
# WATCHLIST
WATCHLIST_SESSION_ID = 'watchlist'

# MESSAGE_STORAGE
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# USER
# AUTH_USER_MODEL = 'user.CustomUser'
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# LOGOUT_REDIRECT_URL = '/'


# CELERY
CELERY_BROKER_URL = 'redis://localhost:6379'  
CELERY_RESULT_BACKEND = 'redis://localhost:6379'  
CELERY_ACCEPT_CONTENT = ['application/json']  
CELERY_RESULT_SERIALIZER = 'json'  
CELERY_TASK_SERIALIZER = 'json'

# CKEDITOR
CKEDITOR_UPLOAD_PATH = "media/uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'height' : 120,
        'width' : 560,
        # 'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
      
            {'name': 'clipboard', 'items': ['Source','Undo', 'Redo']},
            
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat']},
            
            
            {'name': 'insert',
             'items': ['Image', 'Table', 'btgrid','Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

                
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
       
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'btgrid',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}



TELEGRAM_GET_LINK = '/'