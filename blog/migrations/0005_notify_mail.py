# Generated by Django 4.2.7 on 2023-12-31 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_notify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notify_Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='送信日時')),
                ('notify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.notify', verbose_name='メールする通知')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='受信者')),
            ],
        ),
    ]
