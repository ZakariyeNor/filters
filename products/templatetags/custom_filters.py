# products/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def underscore_to_dash(value):
    return value.replace("_", "–")
