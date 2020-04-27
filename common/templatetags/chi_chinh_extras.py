from django import template
from django.conf import settings
from recipes.models import Recipe


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


@register.inclusion_tag('recipes/common/accordion.html')
def accordion(recipe):
    return {'recipe': recipe}


@register.inclusion_tag('recipes/common/archive.html')
def recipe_archive():
    recipe_archive = Recipe.objects.archive()
    return {'recipe_archive': recipe_archive}


@register.inclusion_tag('recipes/common/snippet.html')
def snippet(recipe):
    return {'recipe': recipe}


@register.inclusion_tag('recipes/common/locale_date.html')
def locale_date(lang_code, date):
    return {'lang_code': lang_code, 'date': date}
