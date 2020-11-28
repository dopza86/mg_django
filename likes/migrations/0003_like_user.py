# Generated by Django 3.1.3 on 2020-11-28 15:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('likes', '0002_like_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
