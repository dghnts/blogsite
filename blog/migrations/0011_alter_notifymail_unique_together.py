# Generated by Django 4.2.7 on 2024-01-02 23:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_rename_notify_mail_notifymail'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='notifymail',
            unique_together={('user', 'notify')},
        ),
    ]
