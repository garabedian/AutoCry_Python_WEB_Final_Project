from django.core.exceptions import ValidationError


def year_validator(value):
    if value <= 1900 or value > 2020:
        raise ValidationError('Build year must be between 1900 and 2020!')


def availability_validator(value):
    # from main_app.models import Item
    # total_expenses = sum([expense.price for expense in Expenses.objects.all()])
    # if total_expenses + value > budget:
    #     raise ValidationError('Amount cannot exceed available funds')
    pass