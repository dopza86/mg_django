# Generated by Django 3.1.3 on 2020-12-07 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
            ],
            options={
                'verbose_name': '대화',
                'verbose_name_plural': '대화',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('message', models.TextField()),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='conversations.conversation')),
            ],
            options={
                'verbose_name': '메세지',
                'verbose_name_plural': '메세지',
            },
        ),
    ]
