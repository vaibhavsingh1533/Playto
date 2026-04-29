from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-90$@#brh7_8(^-(o3i7p*4#$++3&8e5q3()qdv9qfqif7#_vhd'

DEBUG = True

ALLOWED_HOSTS = []

# ---------------------------
# INSTALLED APPS
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'payout',
]

# ---------------------------
# MIDDLEWARE (ORDER IMPORTANT)
# ---------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # MUST BE FIRST
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# CORS SETTINGS (FIXED)
# ---------------------------
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with",
    "Idempotency-Key",   # 🔥 VERY IMPORTANT
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "OPTIONS",
]

# ---------------------------
# CSRF SETTINGS
# ---------------------------
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

CSRF_ALLOW_CREDENTIALS = True

# ---------------------------
# URL CONFIG
# ---------------------------
ROOT_URLCONF = 'core.urls'

# ---------------------------
# TEMPLATES
# ---------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ---------------------------
# DATABASE (POSTGRESQL)
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'playto_db',
        'USER': 'postgres',
        'PASSWORD': '8827',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ---------------------------
# PASSWORD VALIDATION
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------
# INTERNATIONALIZATION
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# STATIC FILES
# ---------------------------
STATIC_URL = 'static/'

# ---------------------------
# CELERY (REDIS)
# ---------------------------
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# ---------------------------
# DEFAULT PRIMARY KEY
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'