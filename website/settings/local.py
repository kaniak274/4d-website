from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'local')
]

WEBPACK_MANIFEST_FILE = os.path.join(BASE_DIR, '../webpack-stats.local.json')
