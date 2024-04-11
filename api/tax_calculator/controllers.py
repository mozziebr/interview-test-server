import random
from api.utils import naptime
from .tax_brackets import get_tax_brackets


def get_reliable_brackets():
    return get_tax_brackets()


def calculate_tax(salary, tax_year):
    brackets = get_tax_brackets(str(tax_year))
    total_tax = 0
    tax_bands = []

    for bracket in brackets:
        min_income = bracket['min']
        max_income = bracket.get('max', None)
        rate = bracket['rate']

        if max_income is not None and salary > max_income:
            tax_amount = (max_income - min_income) * rate
        else:
            tax_amount = (salary - min_income) * rate

        total_tax += tax_amount
        tax_bands.append({
            'min_income': min_income,
            'max_income': max_income,
            'tax_rate': rate,
            'tax_amount': tax_amount
        })

        if max_income is not None and salary > max_income:
            break

    effective_rate = total_tax / salary * 100 if salary > 0 else 0

    return total_tax, tax_bands, effective_rate
