from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Recipe, Category


class RecipeAdmin(TranslationAdmin):
    pass


admin.site.register(Category, RecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
