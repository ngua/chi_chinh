from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSiteMap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'
    i18n = True

    def items(self):
        return ['index', 'contact']

    def location(self, item):
        return reverse(item)
