from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Recipe, Category


class RecipeViewTestCase(APITestCase):
    def setUp(self):
        self.yt_id = 'LuNeOuXjkyw'
        for name in 'One', 'Two':
            Category.objects.create(name=name)
        self.recipe_one = Recipe.objects.create(
            name='test',
            description=name,
            picture='test.png',
            url=f'https://youtube.com/watch?v={self.yt_id}'
        )
        self.recipe_two = Recipe.objects.create(
            name='test two',
            description=name,
            picture='test.png',
            url=f'https://www.youtube.com/watch?v={self.yt_id}'
        )
        self.recipe_one.categories.add(Category.objects.first())
        for category in Category.objects.all():
            self.recipe_two.categories.add(category)

    def test_get_request(self):
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_filter(self):
        response = self.client.get(
            reverse('recipe-list') + '?categories=One'
        )
        self.assertEqual(response.data['count'], 2)
        response = self.client.get(
            reverse('recipe-list') + '?categories=Two,One'
        )
        self.assertEqual(response.data['count'], 1)

    def test_embed_regex(self):
        embed, _ = self.recipe_one.get_embed_url()
        self.assertEqual(
            embed,
            f'https://youtube.com/embed/{self.yt_id}'
        )
        embed, _ = self.recipe_two.get_embed_url()
        self.assertEqual(
            embed,
            f'https://youtube.com/embed/{self.yt_id}'
        )
