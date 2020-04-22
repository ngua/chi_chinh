from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer, CategorySerializer
from .filters import RecipeFilter
from .pagination import PageNumberPaginator


def index(request):
    latest = Recipe.objects.order_by('-created')[:2]
    archive = set(Recipe.objects.dates('created', 'year'))
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
    pagination_class = PageNumberPaginator

    def get(self, request, **kwargs):
        response = super().get(request, **kwargs)
        all_categories = Recipe.all_categories()
        serializer = CategorySerializer(all_categories, many=True)
        response.data['all'] = serializer.data
        return response


class RecipeDetailView(DetailView):
    model = Recipe
