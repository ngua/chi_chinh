from django_filters import rest_framework as filters
from .models import Recipe


class RecipeFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='categories__name',
        lookup_expr='iexact'
    )

    class Meta:
        model = Recipe
        fields = ['categories']
