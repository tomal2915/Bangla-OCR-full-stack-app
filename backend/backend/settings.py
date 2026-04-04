import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv(os.path.join(Path(__file__).resolve().parent.parent.parent, '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY    = os.getenv('SECRET_KEY', 'fallback-dev-key-change-in-production')
DEBUG         = os.getenv('DEBUG', 'False') == 'True'

# Include Railway domain + localhost
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1'
).split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'ocr',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',        # ← must be first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← must be right after Security
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000'
).split(',')

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# ── Database ────────────────────────────────────────────────
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     os.getenv('DB_NAME'),
            'USER':     os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST':     os.getenv('DB_HOST', 'localhost'),
            'PORT':     os.getenv('DB_PORT', '5432'),
        }
    }

# ── Media files ─────────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ── ML model paths ──────────────────────────────────────────
# On Railway, set ML_MODEL_PATH and ML_CLASS_MAP as env vars
# pointing to where you uploaded the files (see note below)
ML_MODEL_PATH = os.getenv(
    'ML_MODEL_PATH',
    str(BASE_DIR.parent / 'ml' / 'bangla_ocr.h5')
)
ML_CLASS_MAP = os.getenv(
    'ML_CLASS_MAP',
    str(BASE_DIR.parent / 'ml' / 'class_map.json')
)

# ── Static files ─────────────────────────────────────────────
STATIC_URL  = '/static/'                           # ← only defined once
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES':     [],
}