from rest_framework import serializers
from .models import Recipe, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.CharField())

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        recipe = super().create(validated_data)
        # categories_query = Category.objects.filter(name__in=categories)
        recipe.categories.add(*categories)
        return recipe

    class Meta:
        model = Recipe
        fields = '__all__'
