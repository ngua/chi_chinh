from rest_framework import serializers
from .models import Recipe, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class RecipeSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Recipe
        fields = '__all__'
