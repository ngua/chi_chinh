# Generated by Django 3.0.5 on 2020-04-21 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20200421_0235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-created']},
        ),
    ]