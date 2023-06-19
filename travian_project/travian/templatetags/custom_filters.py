from django import template
import json

register = template.Library()

@register.filter
def json_decode(value):
    return json.loads(value)

register = template.Library()

@register.filter
def get_building_cost(building, level):
    building_cost = building.building_cost
    return building_cost[str(level)] if str(level) in building_cost else None