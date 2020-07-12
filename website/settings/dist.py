from .base import *
from .email import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ALLOWED_HOSTS = []

MANAGERS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'apps': {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        'django': {
            'handlers': ["console"],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'dist')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

WEBPACK_MANIFEST_FILE = os.path.join(BASE_DIR, '../webpack-stats.dist.json')
