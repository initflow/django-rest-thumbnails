from importlib import import_module

from django.conf import settings
from django.core.files.storage import get_storage_class

import os

def import_from_path(cls_path):
    package, name = cls_path.rsplit('.', 1)
    return getattr(import_module(package), name)


# Common configuration

DEFAULT_FILE_SIGNATURE = '%(source)s/%(size)s/%(method)s/%(secret)s%(extension)s'

FILE_SIGNATURE = getattr(settings,
    'THUMBNAILS_FILE_SIGNATURE',
    DEFAULT_FILE_SIGNATURE)

# Client configuration - only used by the template tag

THUMBNAIL_PROXY_BASE_URL = getattr(settings,
    'THUMBNAILS_PROXY_BASE_URL',
    '/thumbnails/')

def thumbnail_proxy():
    THUMBNAIL_PROXY = getattr(settings,
        'THUMBNAILS_PROXY',
        'restthumbnails.proxies.ThumbnailProxy')

    return import_from_path(THUMBNAIL_PROXY)

# Server configuration

DEFAULT_REGEX = r'^%s$' % (FILE_SIGNATURE % {
    'source': r'(?P<source>.+)',
    'size': r'(?P<size>.+)',
    'method': r'(?P<method>.+)',
    'secret': r'(?P<secret>.+)',
    'extension': r'(?P<extension>\..+)',
})

URL_REGEX = getattr(settings,
    'THUMBNAILS_URL_REGEX',
    DEFAULT_REGEX)

LOCK_TIMEOUT = getattr(settings,
    'THUMBNAILS_LOCK_TIMEOUT',
    10)

KEY_PREFIX = getattr(settings,
    'THUMBNAILS_KEY_PREFIX',
    'restthumbnails')

def thumbnail_file():
    THUMBNAIL_FILE = getattr(settings,
        'THUMBNAILS_FILE',
        'restthumbnails.files.ThumbnailFile')

    return import_from_path(THUMBNAIL_FILE)

def response_backend():
    RESPONSE_BACKEND = getattr(settings,
        'THUMBNAILS_RESPONSE_BACKEND',
        'restthumbnails.responses.dummy.sendfile')

    return import_from_path(RESPONSE_BACKEND)

# Storage backends

def source_storage_backend():
    SOURCE_STORAGE_BACKEND = getattr(settings,
        'THUMBNAILS_SOURCE_STORAGE_BACKEND',
        'django.core.files.storage.FileSystemStorage')

    SOURCE_STORAGE_LOCATION = getattr(settings,
        'THUMBNAILS_SOURCE_ROOT',
        settings.MEDIA_ROOT)

    return get_storage_class(SOURCE_STORAGE_BACKEND)(
        location=SOURCE_STORAGE_LOCATION)


def storage_backend():
    STORAGE_BACKEND = getattr(settings,
        'THUMBNAILS_STORAGE_BACKEND',
        'django.core.files.storage.FileSystemStorage')

    STORAGE_LOCATION = getattr(settings,
        'THUMBNAILS_STORAGE_ROOT',
        os.path.join(settings.MEDIA_ROOT, '..', 'thumbnails'))

    STORAGE_BASE_PATH = getattr(settings,
        'THUMBNAILS_STORAGE_BASE_PATH',
        '/thumbnails/')

    return get_storage_class(STORAGE_BACKEND)(
        location=STORAGE_LOCATION,
        base_url=STORAGE_BASE_PATH)
