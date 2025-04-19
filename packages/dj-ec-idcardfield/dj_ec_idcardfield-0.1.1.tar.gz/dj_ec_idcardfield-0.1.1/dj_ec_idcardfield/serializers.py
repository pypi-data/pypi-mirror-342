try:
    from rest_framework import __version__ as drf_version

    from dj_ec_idcardfield import DRF_MIN_VERSION

    drf_version = drf_version.split('.')[:2]
    drf_version = '.'.join(drf_version)
    if float(drf_version) < float(DRF_MIN_VERSION):
        raise ImportError(
            f"Django REST Framework version {drf_version} not supported.")
except ModuleNotFoundError as error:
    raise ModuleNotFoundError(error)

from rest_framework.serializers import CharField

from dj_ec_idcardfield.validators import (
    validate_idcard,
    validate_idcard_or_ruc,
    validate_ruc,
)


class IdcardField(CharField):
    default_error_messages = {'invalid': validate_idcard.message}

    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', validate_idcard.NUMBER_DIGITS)
        kwargs.setdefault('min_length', validate_idcard.NUMBER_DIGITS)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        validate_idcard(data)
        return data


class RUCField(CharField):
    default_error_messages = {'invalid': validate_ruc.message}

    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', validate_ruc.NUMBER_DIGITS)
        kwargs.setdefault('min_length', validate_ruc.NUMBER_DIGITS)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        validate_ruc(data)
        return data


class IdcardOrRUCField(IdcardField, RUCField):
    default_error_messages = {'invalid': validate_idcard_or_ruc.message}

    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', validate_ruc.NUMBER_DIGITS)
        kwargs.setdefault('min_length', validate_idcard.NUMBER_DIGITS)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        validate_idcard_or_ruc(data)
        return data
