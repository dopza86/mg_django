# Generated by Django 3.1.3 on 2020-11-27 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_remove_comment_like'),
        ('likes', '0001_initial'),
        ('posts', '0008_post_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment',
        ),
        migrations.AddField(
            model_name='post',
            name='comment',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_comment', to='comments.Comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_like', to='likes.like'),
        ),
    ]
