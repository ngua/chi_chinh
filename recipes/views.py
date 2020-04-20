from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer
from .filters import RecipeFilter


def index(request):
    latest = Recipe.objects.order_by('-date_posted')[:2]
    archive = set(Recipe.objects.dates('date_posted', 'year'))
    context = {'latest': latest, 'archive': archive}
    return render(request, 'index.html', context=context)


def recipes(request):
    return render(request, 'recipes/recipe_list.html')


class RecipeListAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    filterset_fields = ['categories']
