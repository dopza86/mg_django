# Generated by Django 3.1.3 on 2020-12-03 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_followees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followees',
        ),
    ]
