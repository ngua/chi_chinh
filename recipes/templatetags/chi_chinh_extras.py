from django import template
from django.conf import settings


register = template.Library()


@register.filter
def slice_url(url):
    prefix = url[1:3]
    if prefix not in ['en', 'vi']:
        return url
    return url[3:]


@register.simple_tag
def get_setting(name):
    if name not in settings.SETTINGS_EXPORT:
        raise AttributeError(f'{name} is not in allowed settings exports')
    return getattr(settings, name, '')
