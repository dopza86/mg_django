# Generated by Django 3.1.4 on 2021-01-03 18:09

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('file', models.ImageField(upload_to='post_images', verbose_name='사진 파일')),
            ],
            options={
                'verbose_name': '사진',
                'verbose_name_plural': '사진',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('name', models.CharField(max_length=140, verbose_name='이름')),
                ('location', models.CharField(blank=True, max_length=256, null=True, verbose_name='위치')),
                ('caption', models.TextField(blank=True, default='', verbose_name='설명')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': '포스트',
                'verbose_name_plural': '포스트',
                'ordering': ['-pk'],
            },
        ),
    ]
