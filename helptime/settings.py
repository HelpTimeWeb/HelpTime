# helptime/settings.py
from pathlib import Path
import os
import environ  # pip install django-environ

# -------------------------------------------------------
# Base
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# Leer .env
# -------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False)
)

# Busca un archivo .env en la raíz del proyecto (opcional)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# -------------------------------------------------------
# Seguridad
# -------------------------------------------------------
SECRET_KEY = env('SECRET_KEY', default='clave-por-defecto-para-dev')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = ['helptime.onrender.com', 'localhost', '127.0.0.1']

# -------------------------------------------------------
# Aplicaciones
# -------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'widget_tweaks',
]

AUTH_USER_MODEL = 'core.Usuario'

# -------------------------------------------------------
# Middleware
# -------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # servir estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------------------------------
# URLs y templates
# -------------------------------------------------------
ROOT_URLCONF = 'helptime.urls'

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

WSGI_APPLICATION = 'helptime.wsgi.application'

# -------------------------------------------------------
# Base de datos
# -------------------------------------------------------
DATABASES = {
    'default': env.db(default='postgres://postgres:Helptimecontra77@localhost:5432/postgres')
}

# -------------------------------------------------------
# Password validators
# -------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------
# Internacionalización
# -------------------------------------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------
# Archivos estáticos y media
# -------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------------------------------------
# Login
# -------------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# -------------------------------------------------------
# Default primary key
# -------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
