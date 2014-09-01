#!/usr/bin/env python
#-*- coding:utf-8 -*-


"""
Django settings for iplay_mgmt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bft0dwfsqqiae1bs%0ve+&=v%dxdvs=eg2r5tg^(e!55j@q1bb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [u'192.168.1.65', u'localhost', u'127.0.0.1']

ADMINS = (
    ('xiangxiaowei', 'xiangxiaowei@lbesec.com'),
)

MANAGERS = ADMINS

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'templates',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'market',
    'game',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'iplay_management.urls'

WSGI_APPLICATION = 'iplay_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'admin',
        'USER': 'forum',
        'PASSWORD': 'VQq*d@GY4F7J6]MP',
        'HOST': '192.168.0.1',
        'PORT': '3306'
    },
    'market': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'forum',
        'USER': 'forum',
        'PASSWORD': 'VQq*d@GY4F7J6]MP',
        'HOST': '192.168.0.1',
        'PORT': '3306'
    },
    'game': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'forum',
        'USER': 'forum',
        'PASSWORD': 'VQq*d@GY4F7J6]MP',
        'HOST': '192.168.0.1',
        'PORT': '3306'
    }
}

DATABASE_ROUTERS = ['dbsetings.appdb']

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#    '/opt/www/iplay_mgmt/static',
    ("img", os.path.join(STATIC_ROOT, 'img').replace('\\', '/')),
    ("css", os.path.join(STATIC_ROOT, 'css').replace('\\', '/')),
    ("js", os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
    ("fonts", os.path.join(STATIC_ROOT, 'fonts').replace('\\', '/')),
)

#Home page url
INDEX_URL = 'http://192.168.50.121:8000'
# INDEX_URL = 'http://localhost'

#the database of user_message,user_iplay
ACCOUNT = 'account'

LOTTERY = 'lottery'


# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(name)s %(asctime)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(name)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django_request': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s status_code:%(status_code)d',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django_db_backends': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s duration:%(duration).3f sql:%(sql)s params:%(params)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'custom_log_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'verbose'
        },
        'django_request_logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_request_logfile.log'),
            #you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'django_request'
        },
        'django_db_backends_logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_db_backends_logfile.log'),
            #you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'django_db_backends'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },  
        'market': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/market.log'),
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['custom_log_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'django_request_logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['django_db_backends_logfile', ],
            'level': 'WARNING',
            'propagate': True,
        },
        'customapp': {  #then you can change the level to control your custom app whether to output the debug infomation
                        'handlers': ['console'],
                        'level': 'DEBUG',
                        'propagate': False,
        },
        'market': {
            'handlers': ['market'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
