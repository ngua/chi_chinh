import re
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
        """
        Returns list of model instance creation dates in descending order for
        use in template.

        :returns list: list of instance creation dates
        """
        return [
            date for date in self.dates(
                'created', 'month', order='DESC'
            )
        ]

    @staticmethod
    def all_categories():
        """
        Filters all Category instances with at least one relation m2m relation
        with Recipe instance.

        :returns QuerySet: Category instances
        """
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
        """
        Overrides save method in order to create url slug, checking for
        instance id attribute to avoid later changing slug when instance
        name changes (can cause 404s)
        Also creates dramatiq task to set new attribute to false after
        one week delay

        """
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

    def get_embed_url(self):
        """
        Attempts to match url attribute against YouTube domains and query
        params in order generate both embed video url as well as YT's
        automatically generated video thumbnails.

        :returns tuple: if regex successful, a tuple of strings. Otherwise,
            tuple of two NoneType instances, as this method is always expected
            to always return a pair of values
        """
        pattern = re.compile(
            r'(https://)(?:www\.)?(youtube\.com)/(?:watch\?.*?'
            r'(?=v=)v=|v/|.+\?v=)?([^&=%\?]{11})'
        )
        m = re.match(pattern, self.url)
        try:
            embed = f'{m.group(1)}{m.group(2)}/embed/{m.group(3)}'
            thumbnail = f'https://i3.ytimg.com/vi/{m.group(3)}/hqdefault.jpg'
            return embed, thumbnail
        except AttributeError:
            return None, None

    def get_random_related(self):
        """
        If they exist, attempts to find one Recipe instance belonging to the
        same category for each of object's m2m relations with Category objects.

        TODO: Replace order_by('?') with more efficient algorithm to find
        random db rows - highly inefficient and scales really poorly.

        :returns dict: with Category instance names as keys and Recipe objects
            as values
        """

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
        """
        Displays comma-separated string representation of all related Category
        instances. For use in admin interface.
        """
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
    instance.picture.delete(save=False)
