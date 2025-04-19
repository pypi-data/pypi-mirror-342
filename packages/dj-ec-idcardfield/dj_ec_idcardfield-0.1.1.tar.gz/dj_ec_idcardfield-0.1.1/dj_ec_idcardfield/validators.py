from re import compile as re_compile

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _


class IdcardValidator(RegexValidator):
    NUMBER_DIGITS = 10
    idcard_regex = r'^[0-2]{1}[0-9]{9}'
    regex = re_compile(idcard_regex + '$')
    message = _('Enter a valid number.')
    code = 'invalid'

    def validator(self, value):
        if value == '0000000000':
            raise ValidationError(self.message, code=self.code,
                              params={'value': value})

    def __call__(self, value):
        self.validator(value)
        super().__call__(value)


class RUCValidator(IdcardValidator):
    NUMBER_DIGITS = 13
    ruc_regex = IdcardValidator.idcard_regex + '[0-2]{1}[0-9]{2}'
    regex = re_compile(ruc_regex + '$')

    def validator(self, value):
        if value[-3:] == '000':
            raise ValidationError(self.message, code=self.code,
                              params={'value': value})


class IdcardOrRUCValidator(RUCValidator):
    def set_regex(self, value):
        """Change the regex if the value is Idcard.

        Args:
            value (str): Idcard number or R.U.C.
        """
        if len(value) == IdcardValidator.NUMBER_DIGITS:
            regex = IdcardValidator.regex
        else:
            regex = RUCValidator.regex
        self.regex = _lazy_re_compile(regex, self.flags)


    def __call__(self, value):
        self.set_regex(value)
        if len(value) == IdcardValidator.NUMBER_DIGITS:
            IdcardValidator.validator(self, value)
        elif len(value) == RUCValidator.NUMBER_DIGITS:
            RUCValidator.validator(self, value)
        RegexValidator.__call__(self, value)


validate_idcard = IdcardValidator()

validate_ruc = RUCValidator()

validate_idcard_or_ruc = IdcardOrRUCValidator()
