import os
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import signals
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
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(editable=False)
    url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_random_related(self):
        related = []
        categories = []
        for category in self.categories.all():
            try:
                related.append(Recipe.objects.filter(
                    categories__name__in=[category]
                ).order_by('?').exclude(id=self.id).exclude(
                    id__in=related
                ).first().id)
                categories.append(category)
            except AttributeError:
                pass
        return dict(
            zip(categories, list(Recipe.objects.filter(id__in=related)))
        )

    @staticmethod
    def all_categories():
        return Category.objects.filter(recipe__isnull=False).distinct()

    def __repr__(self):
        return f"{self.__class__.__name__}'({self.name})'"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']


@receiver(signals.post_delete, sender=Recipe)
def auto_delete_pic(sender, instance, **kwargs):
    if instance.picture and os.path.isfile(instance.picture.path):
        os.remove(instance.picture.path)


@receiver(signals.pre_save, sender=Recipe)
def remove_updated_pic(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Recipe.objects.get(id=instance.pk).picture
    except Recipe.DoesNotExist:
        return

    new = instance.picture
    if new != old and os.path.isfile(new):
        os.remove(old)
