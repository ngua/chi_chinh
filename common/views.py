from django.shortcuts import render
from recipes.models import Recipe


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
