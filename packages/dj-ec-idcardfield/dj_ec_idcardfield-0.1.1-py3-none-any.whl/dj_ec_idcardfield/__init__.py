__version__ = '0.1.1'

DJANGO_MIN_VERSION = '4.2'

DRF_MIN_VERSION = '3.14'

try:
    from django.utils.version import get_docs_version

    django_version = get_docs_version()
    if float(django_version) < float(DJANGO_MIN_VERSION):
        raise ImportError(f"Django version {django_version} not supported.")
except ModuleNotFoundError as error:
    raise ModuleNotFoundError(error)
