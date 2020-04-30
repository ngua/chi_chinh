import os
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.db.models import signals
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from .tasks import unmark_new_task


class RecipeManager(models.Manager):
    def archive(self):
        return [
            date for date in self.dates(
                'created', 'month', order='DESC'
            )
        ]

    @staticmethod
    def all_categories():
        return Category.objects.filter(recipe__isnull=False).distinct()


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __repr__(self):
        return f"Category('{self.name}')"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = RichTextField(_('description'))
    picture = models.ImageField(
        _('picture'), upload_to=settings.RECIPE_PIC_PATH
    )
    featured = models.BooleanField(_('featured'), default=False)
    new = models.BooleanField(_('new'), default=True)
    created = models.DateField(_('created'), default=timezone.now)
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'))
    slug = models.SlugField(_('slug'), editable=False)
    url = models.URLField('URL', blank=True)

    objects = RecipeManager()

    def get_absolute_url(self):
        return reverse(
            'recipe-detail',
            kwargs={
                'year': self.created.strftime('%Y'),
                'month': self.created.strftime('%m'),
                'slug': self.slug
            }
        )

    def save(self, *args, **kwargs):
        create_task = False
        if not self.id:
            self.slug = slugify(self.name)
            create_task = True
        super().save(*args, **kwargs)
        if create_task:
            unmark_new_task.send_with_options(
                args=[self.id],
                delay=int(6.048e+8)
            )

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

    def display_categories(self):
        return ', '.join([str(category) for category in self.categories.all()])

    def __repr__(self):
        return f"Recipe('{self.name}', '{self.picture}')"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
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
