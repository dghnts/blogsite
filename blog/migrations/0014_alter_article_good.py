# Generated by Django 4.2.7 on 2024-01-08 03:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0013_delete_notifymail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='good',
        ),
        migrations.AddField(
            model_name='article',
            name='good',
            field=models.ManyToManyField(blank=True, related_name='good_user', to=settings.AUTH_USER_MODEL, verbose_name='いいね'),
        ),
    ]
