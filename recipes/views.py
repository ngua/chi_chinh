from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.sites.models import Site
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Recipe
from .serializers import RecipeSerializer, CategorySerializer
from .filters import RecipeFilter
from .pagination import PageNumberPaginator


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def recipes(request):
    return render(request, 'recipes/recipe_list.html')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class RecipeListAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    filterset_fields = ['categories']
    pagination_class = PageNumberPaginator

    def get(self, request, **kwargs):
        response = super().get(request, **kwargs)
        all_categories = Recipe.objects.all_categories()
        serializer = CategorySerializer(all_categories, many=True)
        response.data['all'] = serializer.data
        return response


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class RecipeDetailView(DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related = self.object.get_random_related()
        embed_url, thumbnail = self.object.get_embed_url()
        context['related'] = related
        context['embed_url'] = embed_url
        context['thumbnail'] = thumbnail
        context['domain'] = Site.objects.get_current().domain
        return context


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class RecipeArchiveView(ArchiveIndexView):
    queryset = Recipe.objects.order_by('created')
    date_field = 'created'
    allow_empty = True


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class RecipeMonthArchiveView(MonthArchiveView):
    queryset = Recipe.objects.order_by('created')
    date_field = 'created'
    allow_empty = True
    allow_future = True
