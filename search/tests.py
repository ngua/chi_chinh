from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, Category


class SearchTestCase(TestCase):
    def setUp(self):
        cat1 = Category.objects.create(name_en='Western')
        cat2 = Category.objects.create(name_en='Vietnamese')
        cat2.name_vn = 'Việt'
        self.recipe1 = Recipe.objects.create(
                name='Tortillas',
                description='',
                picture='test.png',
            )
        self.recipe2 = Recipe.objects.create(
                name='Mì xào',
                description='This is Vietnamese food.',
                picture='test.png',
            )
        self.recipe1.categories.add(cat1)
        self.recipe2.categories.add(cat2)

    def test_category_search(self):
        response = self.client.get(reverse('search') + '?q=western')
        self.assertContains(response, self.recipe1.categories.first())

    def test_fuzzy_trigram_search(self):
        response = self.client.get(reverse('search') + '?q=mi+xao')
        self.assertContains(response, self.recipe2.categories.first())

    def test_i18n_search(self):
        response = self.client.get(reverse('search') + '?q=Việt')
        self.assertContains(response, self.recipe2.categories.first())

    def test_description_search(self):
        response = self.client.get(reverse('search') + '?q=food')
        self.assertContains(response, self.recipe2.name)
