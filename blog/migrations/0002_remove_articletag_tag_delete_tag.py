# Generated by Django 4.2.7 on 2023-12-03 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articletag',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
