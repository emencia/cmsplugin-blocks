# Available default templates
BLOCKS_ALBUM_TEMPLATES = [
    ('cmsplugin_blocks/album/default.html', 'Default'),
]

BLOCKS_CARD_TEMPLATES = [
    ('cmsplugin_blocks/card/default.html', 'Default'),
]

BLOCKS_HERO_TEMPLATES = [
    ('cmsplugin_blocks/hero/default.html', 'Default'),
]

BLOCKS_SLIDER_TEMPLATES = [
    ('cmsplugin_blocks/slider/default.html', 'Default'),
]

# Temporary directory where to store zip files for item mass upload
BLOCKS_TEMP_DIR = 'temp/'

# Allowed image file extension for basic validation in mass upload from ZIP
# file
BLOCKS_MASSUPLOAD_IMAGE_TYPES = [
    'jpg',
    'jpeg',
    'svg',
    'gif',
    'png',
]

# Maximum file size allowed for mass upload feature
# This is a limit at Django level so file will still be processed, you may
# think to set a limit also at server level to avoid basic attacks with very
# big files.
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
#BLOCKS_MASSUPLOAD_FILESIZE_LIMIT = 5242880 # 5MiO
#BLOCKS_MASSUPLOAD_FILESIZE_LIMIT = 104857600 # 10MiO
BLOCKS_MASSUPLOAD_FILESIZE_LIMIT = 429916160 # 50MiO
