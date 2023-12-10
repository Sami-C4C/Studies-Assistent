from django import template

register = template.Library()


@register.filter(name='chr')
def chr_filter(value):
    return chr(int(value))
