import sys

from texsite.application.config import DATA_ROOT
from texsite.settings.base import *  # noqa: F401, F403


DEBUG = False

try:
    sys.path.append(str(DATA_ROOT))
    from localsettings import *  # noqa: F401, F403
except ImportError:
    pass
