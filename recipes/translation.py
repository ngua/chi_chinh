from modeltranslation.translator import register, TranslationOptions
from .models import Recipe, Category


@register(Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en',)
