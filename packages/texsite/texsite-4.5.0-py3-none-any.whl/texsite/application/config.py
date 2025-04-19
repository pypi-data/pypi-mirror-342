import os
from pathlib import Path


PACKAGE_ROOT = Path(__file__).parent
DATA_ROOT = Path(os.environ.get('TEXSITE_DATA_ROOT', './.data'))
