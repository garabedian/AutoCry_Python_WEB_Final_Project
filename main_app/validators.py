from django.core.exceptions import ValidationError


def budget_validator(value):
    if value <= 0:
        raise ValidationError('Amount cannot be zero or negative')


def availability_validator(value):
    # from main_app.models import Item
    # total_expenses = sum([expense.price for expense in Expenses.objects.all()])
    # if total_expenses + value > budget:
    #     raise ValidationError('Amount cannot exceed available funds')
    pass