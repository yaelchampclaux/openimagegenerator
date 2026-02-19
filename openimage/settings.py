"""
Django settings for openimage project.
"""

from pathlib import Path
import os
# from django.core.management.utils import get_random_secret_key

from decouple import config   # type: ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Use environment variable or generate a random secret key
SECRET_KEY = config('SECRET_KEY', 'django-insecure-z9&v=n+=r7$f2v_+t@_itk3d45@#@+1vg&7v@)ofy(4jvpbche')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']  # Allow all hosts for development in Docker

# Application definition
INSTALLED_APPS = [
    # Django's default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'you_image_generator',
]

# Add debug toolbar only in DEBUG mode
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add debug toolbar middleware only in DEBUG mode
if DEBUG and 'debug_toolbar' in INSTALLED_APPS:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'openimage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'openimage.wsgi.application'

# Database - Parse DATABASE_URL manually if provided
DATABASE_URL = config('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    # Simple manual parsing of postgres://user:password@host:port/database
    import re
    match = re.match(r'postgres://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', DATABASE_URL)
    if match:
        user, password, host, port, database = match.groups()
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': database,
                'USER': user,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
            }
        }
    else:
        # Fallback to individual env vars if parsing fails
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME', 'openimage_db'),
                'USER': config('DB_USER', 'openimage_user'),
                'PASSWORD': config('DB_PASSWORD', 'your_very_strong_password1234'),
                'HOST': config('DB_HOST', 'db'),
                'PORT': config('DB_PORT', '5432'),
            }
        }
else:
    # Use individual environment variables or SQLite for development
    if DEBUG and not DATABASE_URL:
        # Use SQLite for quick development if no PostgreSQL is configured
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME', 'openimage_db'),
                'USER': config('DB_USER', 'openimage_user'),
                'PASSWORD': config('DB_PASSWORD', 'your_very_strong_password1234'),
                'HOST': config('DB_HOST', 'db'),
                'PORT': config('DB_PORT', '5432'),
            }
        }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Debug Toolbar settings (only if in DEBUG mode)
if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16',
        '0.0.0.0',  # For Docker
    ]
    
# Add Docker gateway IP
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += ['.'.join(ip.split('.')[:-1] + ['1']) for ip in ips]

# === FREE APIs ===
POLLINATION_API_KEY = os.getenv('POLLINATION_API_KEY')
HUGGINGFACE_API_KEY = config('HUGGINGFACE_API_KEY')
SEGMIND_API_KEY = os.getenv('SEGMIND_API_KEY')

# === PAID APIs ===
DEEPAI_API_KEY = config('DEEPAI_API_KEY')
GEMINI_API_KEY = config('GEMINI_API_KEY')
STABILITY_AI_API_KEY = config('STABILITY_AI_API_KEY')
RUNWARE_API_KEY = config('RUNWARE_API_KEY')
REPLICATE_API_KEY = config('REPLICATE_API_KEY')

# Default provider
DEFAULT_IMAGE_PROVIDER = config('DEFAULT_IMAGE_PROVIDER', 'pollinations')
DEFAULT_IMAGE_GENERATION_MODEL = config('DEFAULT_IMAGE_GENERATION_MODEL', 'core')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO' if DEBUG else 'WARNING',
        },
        'you_image_generator': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}