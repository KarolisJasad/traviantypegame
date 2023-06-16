from django import template
import json

register = template.Library()

@register.filter
def json_decode(value):
    return json.loads(value)