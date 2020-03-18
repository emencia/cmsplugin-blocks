"""
Django settings for tests
"""
from sandbox.settings.base import *

DATABASES = {
    # Development default database engine use sqlite3
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'db', 'tests.sqlite3'),
        'TEST': {
            'NAME': os.path.join(DATA_DIR, 'db', 'tests.sqlite3'),  # noqa
        }
    }
}

from cmsplugin_blocks.settings import *
