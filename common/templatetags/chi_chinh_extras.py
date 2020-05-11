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


@register.inclusion_tag('common/tags/lang_form.html', takes_context=True)
def lang_form(context, id_, selector, **kwargs):
    return {
        'id': id_,
        'selector': selector,
        'kwargs': kwargs,
        'csrf': context.get('csrf_token', '')
    }


@register.inclusion_tag('common/tags/accordion.html')
def accordion(recipe):
    return {'recipe': recipe}


@register.inclusion_tag('common/tags/archive.html')
def recipe_archive():
    recipe_archive = Recipe.objects.archive()
    return {'recipe_archive': recipe_archive}


@register.inclusion_tag('common/tags/snippet.html')
def snippet(recipe):
    return {'recipe': recipe}


@register.inclusion_tag('common/tags/locale_date.html')
def locale_date(lang_code, date):
    return {'lang_code': lang_code, 'date': date}


@register.inclusion_tag('common/tags/breadcrumb.html')
def breadcrumb(name):
    return {'name': name}


@register.inclusion_tag('common/tags/breadcrumb_link.html')
def breadcrumb_link(name, location):
    return {'name': name, 'location': location}


@register.inclusion_tag('common/tags/label.html')
def label(content, selector=''):
    return {'content': content, 'selector': selector}


@register.inclusion_tag('common/tags/srcdoc.html')
def srcdoc(embed_url, thumbnail):
    return {'embed_url': embed_url, 'thumbnail': thumbnail}
