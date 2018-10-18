from django.template import Library

register = Library()


@register.filter
def xj(value, a):
    return value * a


@register.filter
def phone(value):

    return value[:3] + "****" + value[-4:]
