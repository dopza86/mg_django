# Generated by Django 3.1.3 on 2020-11-19 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_remove_post_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('post', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='posts.post')),
                ('user', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '좋아요',
                'verbose_name_plural': '좋아요',
            },
        ),
    ]
