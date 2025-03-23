from motor.motor_asyncio import AsyncIOMotorClient
from mongoengine import connect
from dotenv import load_dotenv
from pathlib import Path
import os 
from pathlib import Path
from django.core.management.utils import get_random_secret_key


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "shutr-backend-production.up.railway.app",
    "localhost",
    "127.0.0.1"
]

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'core',
    'portfolio',
    'chat',
    'djoser',
    'social_django',
    'user',
    'booking',
    'vertex_multimodaling',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shutr_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shutr_backend.wsgi.application'

# Redis as the channel layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Redis server
        },
    },
}

# Dummy db for Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# MongoDB Configuration
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGO_CLUSTER_URL = os.getenv('MONGO_CLUSTER_URL')
MONGO_CLUSTER_NAME = os.getenv('MONGO_CLUSTER_NAME')

MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DB_NAME}?retryWrites=true&w=majority&appName={MONGO_CLUSTER_NAME}"

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Establish Connection
connect(db.name, host=MONGO_URI)

#Email Settings
EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL= os.getenv('AWS_SES_FROM_EMAIL')

AWS_SES_ACCESS_KEY_ID = os.getenv('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.getenv('AWS_SES_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION_NAME')
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
AWS_SES_FROM_EMAIL = os.getenv('AWS_SES_FROM_EMAIL')
USE_SES_V2 = True

DOMAIN= os.getenv('DOMAIN')
SITE_NAME= 'SHUTR'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
SECRET_ROOT= BASE_DIR / 'static'
MEDIA_URL= 'media/'
MEDIA_ROOT= BASE_DIR / 'media'

SECRET_ROOT = BASE_DIR / 'static'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated'
    # ]
}

DJOSER= {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': os.getenv('REDIRECT_URLS').split(',')
}

AUTH_COOKIE = 'access'
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24
AUTH_COOKIE_SECURE = False
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'Lax'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_AUTH_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_AUTH_SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FACEBOOK_AUTH_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FACEBOOK_AUTH_SECRET_KEY')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email, first_name, last_name'
}
GOOGLE_PROJECT_ID= os.getenv('GOOGLE_PROJECT_ID')
GOOGLE_REGION= os.getenv('GOOGLE_REGION')
VECTOR_INDEX_ID= os.getenv('VECTOR_INDEX_ID')
DEPLOYED_INDEX_ID= os.getenv('DEPLOYED_INDEX_ID')

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GOOGLE_CLIENT_ID = '35440314571-ktdqppuvs0a53fan7f7tfsa4ch76m6bi.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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' 

import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
