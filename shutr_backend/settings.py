from motor.motor_asyncio import AsyncIOMotorClient
from mongoengine import connect
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv() # Load .env file

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u14%zfuh!(@^fj(bc0e@7n*hi&9yvf!h7nl(8(ahl()1^&6t^1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Allow frontend to access the API
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

# client = AsyncIOMotorClient(MONGO_URI)
# db = client[MONGO_DB_NAME]

# Establish Connection
connect(MONGO_DB_NAME, host=MONGO_URI)

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

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# # AWS S3 Configuration
# AWS_ACCESS_KEY_ID = 'your-aws-access-key-id'
# AWS_SECRET_ACCESS_KEY = 'your-aws-secret-access-key'
# AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
# AWS_S3_REGION_NAME = 'your-region'  # e.g. 'us-east-1'



# # Use S3 for storing static files
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# # Optional: Configure the base URL to use for the S3 files
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



