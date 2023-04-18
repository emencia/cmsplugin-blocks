"""
Django settings for tests
"""
from sandbox.settings.base import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Media directory dedicated to tests to avoid polluting other environment
# media directory
MEDIA_ROOT = VAR_PATH / "media-tests"  # noqa: F405

# Require sorl thumbnail to raise exception on errors to ensure tests fail
THUMBNAIL_DEBUG = True

# Available CMS page template for tests purposes only
TEST_PAGE_TEMPLATES = "pages/test.html"
CMS_TEMPLATES.append(  # noqa: F405
    (TEST_PAGE_TEMPLATES, "test-basic"),
)


# Fill cmsplugin blocks settings for test only
BLOCKS_ALBUM_FEATURES = [
    ("foo", "Foo"),
    ("bar", "Bar"),
]

BLOCKS_ALBUMITEM_FEATURES = [
    ("foo", "Foo"),
    ("bar", "Bar"),
]

BLOCKS_CARD_FEATURES = [
    ("foo", "Foo"),
    ("bar", "Bar"),
]

BLOCKS_CONTAINER_FEATURES = [
    ("foo", "Foo"),
    ("bar", "Bar"),
]

BLOCKS_HERO_FEATURES = [
    ("foo", "Foo"),
    ("bar", "Bar"),
]

BLOCKS_SLIDER_FEATURES = [
    ("foo", "Foo"),
    ("bar", "Bar"),
]

BLOCKS_SLIDERITEM_FEATURES = [
    ("foo", "Foo"),
    ("bar", "Bar"),
]

# Add required template for test at the top at the list (so they are the
# default ones picked up by tests)
BLOCKS_ALBUM_TEMPLATES = [
    ("cmsplugin_blocks/album/test.html", "Test"),
] + BLOCKS_ALBUM_TEMPLATES  # noqa: F405

BLOCKS_CARD_TEMPLATES = [
    ("cmsplugin_blocks/card/test.html", "Test"),
] + BLOCKS_CARD_TEMPLATES  # noqa: F405

BLOCKS_CONTAINER_TEMPLATES = [
    ("cmsplugin_blocks/container/test.html", "Test"),
] + BLOCKS_CONTAINER_TEMPLATES  # noqa: F405

BLOCKS_HERO_TEMPLATES = [
    ("cmsplugin_blocks/hero/test.html", "Test"),
] + BLOCKS_HERO_TEMPLATES  # noqa: F405

BLOCKS_SLIDER_TEMPLATES = [
    ("cmsplugin_blocks/slider/test.html", "Test"),
] + BLOCKS_SLIDER_TEMPLATES  # noqa: F405
