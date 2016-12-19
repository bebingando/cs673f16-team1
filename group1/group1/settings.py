"""
Django settings for group1 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import settings
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import settings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lw_pukawrvc*rfw^x6ccq$%vs3rxtu8+6_lodf)j&jo$mjqq%_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Email setting, adding by Zhi and Nora
EMAIL_HOST = 'smtp.live.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'zhidou@hotmail.com'
EMAIL_HOST_PASSWORD = 'DOUZhi19910617'
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True






# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_jenkins',    
    'rest_framework',
    'requirements',
    'comm',
    'issue_tracker',
    'corsheaders',
        'storages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'group1.middleware.SessionSecurityMiddleware',
)

ROOT_URLCONF = 'group1.urls'

WSGI_APPLICATION = 'group1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../database/db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../static'))

LOGIN_URL = '/signin'

CORS_ALLOW_HEADER = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'accept-encoding',
)


EXPIRE_TIME = getattr(settings, 'SESSION_SECURITY_EXPIRE_AFTER', 30)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
"""
Django settings for group1 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lw_pukawrvc*rfw^x6ccq$%vs3rxtu8+6_lodf)j&jo$mjqq%_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Email setting, adding by Zhi and Nora
EMAIL_HOST = 'smtp.live.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'zhidou@hotmail.com'
EMAIL_HOST_PASSWORD = 'DOUZhi19910617'
EMAIL_USE_TLS = True



# session secure added by Zhi Dou and Nora
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
EXPIRE_TIME = getattr(settings, 'SESSION_SECURITY_EXPIRE_AFTER', 600)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

#os.environ['wsgi.url_scheme'] = 'https'

# when boto uploads files to S3, sets properties so when served by S3, includes those HTTP headers in response
# HTTP headers will tell browsers to cache files for specified time
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

# AWS settings
AWS_STORAGE_BUCKET_NAME = 'cs673'
AWS_ACCESS_KEY_ID = 'AKIAJ4K2XB3J24N6UJ7A'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep it simple - just use this domain
# plus the path. (If this isn't set, things get complicated).  This controls how the `static` template tag from
# `staticfiles` gets expanded, if you're using it.  We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when you run `collectstatic`).
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'group1.custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'group1.custom_storages.MediaStorage'
