# Generated by Django 3.0.5 on 2020-04-30 08:23

import ckeditor.fields
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):


    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=100, null=True, unique=True, verbose_name='name')),
                ('name_vi', models.CharField(max_length=100, null=True, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('description', ckeditor.fields.RichTextField(verbose_name='description')),
                ('picture', models.ImageField(upload_to='recipe', verbose_name='picture')),
                ('slug', models.SlugField(editable=False, verbose_name='slug')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('categories', models.ManyToManyField(to='recipes.Category', verbose_name='Categories')),
                ('created', models.DateField(default=django.utils.timezone.now, verbose_name='created')),
                ('description_en', ckeditor.fields.RichTextField(null=True, verbose_name='description')),
                ('description_vi', ckeditor.fields.RichTextField(null=True, verbose_name='description')),
                ('name_en', models.CharField(max_length=100, null=True, unique=True, verbose_name='name')),
                ('name_vi', models.CharField(max_length=100, null=True, unique=True, verbose_name='name')),
                ('featured', models.BooleanField(default=False, verbose_name='featured')),
                ('new', models.BooleanField(default=True, verbose_name='new')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            }
        )
    ]
