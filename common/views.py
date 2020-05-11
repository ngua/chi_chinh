from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from recipes.models import Recipe


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
@csrf_exempt
def index(request):
    latest = Recipe.objects.order_by('-created')[:5]
    featured_recipes = Recipe.objects.filter(featured=True)
    context = {'latest': latest, 'featured_recipes': featured_recipes}
    return render(request, 'common/index.html', context=context)


# Errors

def handler_404(request, exception):
    status = 404
    return render(request, 'common/errors/404.html', {'status': status})


def handler_403(request, exception):
    status = 403
    return render(request, 'common/errors/403.html', {'status': status})


def handler_500(request):
    status = 500
    return render(request, 'common/errors/500.html', {'status': status})
