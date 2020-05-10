from django_filters import rest_framework as filters
from .models import Recipe


class RecipeFilter(filters.FilterSet):
    categories = filters.CharFilter(
        field_name='categories__name',
        method='get_categories'
    )

    def get_categories(self, queryset, field_name, value):
        """
        Method that allows categories parameter to accept multiple comma-
        separated values to filter Category model instances against

        e.g `?categories=example1,example2,example3`
        """
        if not value:
            return queryset
        for category in value.split(','):
            queryset = queryset.filter(categories__name__in=[category])
        return queryset

    class Meta:
        model = Recipe
        fields = ['categories']
