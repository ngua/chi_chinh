from django.shortcuts import render
from recipes.models import Recipe


def index(request):
    latest = Recipe.objects.order_by('-created')[:5]
    featured = Recipe.objects.filter(featured=True)
    context = {'latest': latest, 'featured': featured}
    return render(request, 'common/index.html', context=context)
