# Generated by Django 4.2.7 on 2023-12-31 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_notify_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='subject',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='表題'),
        ),
    ]
