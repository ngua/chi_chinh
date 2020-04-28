from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Recipe, Category


@admin.register(Recipe)
class RecipeAdmin(TranslationAdmin):
    list_display = ('name', 'display_categories')
    list_filter = ('categories',)

    class Meta:
        ordering = ('-created',)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass
