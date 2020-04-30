from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_trigram_extension')
    ]

    operations = [
        UnaccentExtension()
    ]
