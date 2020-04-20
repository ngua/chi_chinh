from datetime import datetime
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __repr__(self):
        return f"{self.__class__.__name__}'({self.name})'"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = RichTextField()
    picture = models.ImageField(
        default='default.png', upload_to=settings.RECIPE_PIC_PATH
    )
    date_posted = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(editable=False)
    url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @staticmethod
    def all_categories():
        return Category.objects.filter(recipe__isnull=False)

    def __repr__(self):
        return f"{self.__class__.__name__}'({self.name})'"

    def __str__(self):
        return self.name
