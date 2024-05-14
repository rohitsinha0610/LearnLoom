# custom_filters.py
from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """
    Custom template filter to subtract arg from value.
    """
    return arg - value
