import sys

from texsite.application.config import DATA_ROOT
from texsite.settings.base import *  # noqa: F401, F403


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&@#s()$&74f78_ve9wkn0deca3&d1pnp*80y3ffoe3mij$_y*@'

# Other settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

try:
    sys.path.append(str(DATA_ROOT))
    from localsettings import *  # noqa: F401, F403
except ImportError:
    pass
