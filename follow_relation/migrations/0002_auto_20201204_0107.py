# Generated by Django 3.1.3 on 2020-12-03 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('follow_relation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='followrelation',
            options={'verbose_name': '팔로우', 'verbose_name_plural': '팔로우'},
        ),
        migrations.AlterField(
            model_name='followrelation',
            name='followee',
            field=models.ManyToManyField(related_name='followee', to=settings.AUTH_USER_MODEL, verbose_name='팔로워'),
        ),
        migrations.AlterField(
            model_name='followrelation',
            name='follower',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='유저'),
        ),
    ]
