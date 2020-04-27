from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Recipe, Category


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_categories')
    list_filter = ('categories',)

    class Meta:
        ordering = ('-created',)


class RecipeTranslationAdmin(RecipeAdmin, TranslationAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field


class CategoryAdmin(TranslationAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
