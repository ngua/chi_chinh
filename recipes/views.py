from django.shortcuts import render
from django.views.generic import ListView
from .models import Recipe


def index(request):
    latest = Recipe.objects.order_by('-date_posted')[:2]
    archive = set(Recipe.objects.dates('date_posted', 'year'))
    context = {'latest': latest, 'archive': archive}
    return render(request, 'index.html', context=context)


class RecipeListView(ListView):
    model = Recipe
