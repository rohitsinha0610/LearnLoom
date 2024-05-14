# __init__.py
# Register custom template tags/filters
from django.template import Library

register = Library()

from . import custom_filters
