from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from dj_ec_idcardfield.forms import (
    IdcardField as FormIdcardField,
    IdcardOrRUCField as FormIdcardOrRUCField,
    RUCField as FormRUCField,
)
from dj_ec_idcardfield.validators import (
    validate_idcard,
    validate_idcard_or_ruc,
    validate_ruc,
)


class IdcardField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', validate_idcard.NUMBER_DIGITS)
        kwargs.setdefault('validators', [validate_idcard, ])
        kwargs.setdefault('verbose_name', _('Idcard'))
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': FormIdcardField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class RUCField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', validate_ruc.NUMBER_DIGITS)
        kwargs.setdefault('validators', [validate_ruc, ])
        kwargs.setdefault('verbose_name', _('RUC'))
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': FormRUCField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class IdcardOrRUCField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', validate_ruc.NUMBER_DIGITS)
        kwargs.setdefault('validators', [validate_idcard_or_ruc, ])
        kwargs.setdefault('verbose_name', _('Idcard or RUC'))
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': FormIdcardOrRUCField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
