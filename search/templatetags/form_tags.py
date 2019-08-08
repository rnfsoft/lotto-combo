from django import template
import re
register = template.Library()

@register.filter
def dash_numbers(numbers):
    numbers = ' - '.join(re.findall(r'\d+', numbers))
    return numbers

