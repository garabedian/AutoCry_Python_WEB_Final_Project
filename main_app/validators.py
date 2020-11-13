from django.core.exceptions import ValidationError


def year_validator(value):
    if value <= 1900 or value > 2020:
        raise ValidationError('Build year must be between 1900 and 2020!')

