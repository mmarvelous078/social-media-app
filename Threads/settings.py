
# DEPLOYMENT SECT #

import dj_database_url

# DEPLOYMENT SECT #
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


#                                                                                            DEPLOYMENT
SECRET_KEY = os.environ.get("SECRET_KEY")
#                                                                                            DEPLOYMENT

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-_b7u_4!nge9)qc)z*sxt+pi&kyt&-pvw-0r)+!jfkuco3kvdv)'

#                                                                                            DEPLOYMENT  
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
#                                                                                            DEPLOYMENT                           

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

#                                                                                            DEPLOYMENT
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
#                                                                                            DEPLOYMENT 

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Threads.urls'

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

WSGI_APPLICATION = 'Threads.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#                                                                                                                        DEPLOYMENT SECTION                                        #
database_url = os.environ.get("DATABASE_URL")
DATABASES["default"] = dj_database_url.parse(database_url)

#postgres://o2_db_uj5m_user:ZMqyYevTf3plh1R6DFhhEtIaHB5WLvPG@dpg-cll0susjtl8s73f51hcg-a.oregon-postgres.render.com/o2_db_uj5m

#                                                                                                                         DEPLOYMENT SECTION                                        #

# DATABASES["default"] = dj_database_url.parse('postgres://o2_db_uj5m_user:ZMqyYevTf3plh1R6DFhhEtIaHB5WLvPG@dpg-cll0susjtl8s73f51hcg-a.oregon-postgres.render.com/o2_db_uj5m')


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Add your BASE_DIR here
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
