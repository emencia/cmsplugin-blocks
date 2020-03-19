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

# Media directory dedicated to tests
MEDIA_ROOT = os.path.join(DATA_DIR, "media-tests")

# Require thumbnail to raise exception on errors to ensure tests fail
THUMBNAIL_DEBUG = True

from cmsplugin_blocks.settings import *
