# Generated by Django 3.0.5 on 2020-04-19 10:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20200419_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
