from django.contrib.sitemaps import Sitemap
from .models import Recipe


class RecipeSitemap(Sitemap):
    changefreq = ''
    priority = 0.9
    i18n = True

    def items(self):
        return Recipe.objects.all()

    def lastmod(self, obj):
        return obj.created
