from django import template

register = template.Library()

@register.filter(name="multiply")
def multiply(value, n):
    return float(value * n)