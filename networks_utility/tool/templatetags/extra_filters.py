from django import template
register = template.Library()

print('hello_from_template')

@register.filter(name='removeDomain')
def removeDomain(value):
    res = value.split('@')[0]
    return res