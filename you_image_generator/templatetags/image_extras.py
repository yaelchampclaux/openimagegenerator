import base64 as base64_module
from django import template

register = template.Library()

@register.filter
def base64(value):
    """Convert bytes to base64 string for displaying images."""
    if value:
        return base64_module.b64encode(value).decode('utf-8')
    return ''