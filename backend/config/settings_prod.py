# Django settings for production environment on Render.

import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ─────────────────────────────────────────────────────────
SECRET_KEY   = os.environ['SECRET_KEY']        # must be set in Render dashboard
DEBUG        = False
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost'
).split(',')

# ── Applications ─────────────────────────────────────────────────────
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

# ── Middleware ────────────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# ── Database (Render PostgreSQL) ──────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',       # Render sets this automatically
        conn_max_age=600,
        ssl_require=True,         # Render requires SSL on PostgreSQL
    )
}

# ── CORS (allow your Render React URL) ───────────────────────────────
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    ''
).split(',')

# also allow all origins during initial testing — remove after confirmed working
# CORS_ALLOW_ALL_ORIGINS = True

# ── Static files (whitenoise serves these on Render) ─────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Media files ───────────────────────────────────────────────────────
# Note: Render free tier has no persistent disk —
# uploaded images will be lost on redeploy.
# For production, replace this with Cloudinary or AWS S3.
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── ML model paths ───────────────────────────────────────────────────
MODEL_PATH  = BASE_DIR / 'bangla_ocr.h5'
LABELS_PATH = BASE_DIR / 'class_labels.json'

# ── Security headers (important for production) ───────────────────────
SECURE_BROWSER_XSS_FILTER       = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
X_FRAME_OPTIONS                 = 'DENY'
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_SECONDS             = 31536000   # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_PRELOAD             = True

# ── Password validation ───────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Logging (errors appear in Render's log dashboard) ─────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'