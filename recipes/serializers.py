from rest_framework import serializers
from .models import Recipe, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class RecipeSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.CharField())
    # Adds absolute url of object in oder to avoid hardcoding path in React
    # component
    absurl = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
