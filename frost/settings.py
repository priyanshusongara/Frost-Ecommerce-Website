"""
Django settings for frost project (PRODUCTION READY)
"""

from pathlib import Path
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = 'django-insecure-CHANGE-THIS-IN-PRODUCTION'

DEBUG = False

ALLOWED_HOSTS = ['frost-996m.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://frost-996m.onrender.com']

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cloudinary',
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
]

# =========================
# CLOUDINARY CONFIG
# =========================
cloudinary.config(
    cloud_name='du7ckl6bt',
    api_key='574553989435262',
    api_secret='YM5gQeRS9gRf2TQDhUitCFriW0g'
)



# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'frost.urls'
WSGI_APPLICATION = 'frost.wsgi.application'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

# =========================
# DATABASE
# =========================
import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get("DATABASE_URL")
    )
}
AUTH_USER_MODEL = 'accounts.Account'

# =========================
# STATIC FILES (WHITE NOISE)
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# MEDIA FILES (CLOUDINARY)
# =========================

# =========================
# OTHER SETTINGS
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# =========================
# EMAIL
# =========================
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
#EMAIL_HOST_USER = 'priyanshusongara23@gmail.com'
#EMAIL_HOST_PASSWORD = 'YOUR_APP_PASSWORD'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# =========================
# RAZORPAY
# =========================
