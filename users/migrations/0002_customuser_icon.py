# Generated by Django 4.2.7 on 2024-01-07 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='users/custom_user/icon/', verbose_name='アイコン'),
        ),
    ]