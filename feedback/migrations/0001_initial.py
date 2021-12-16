# Generated by Django 3.2.8 on 2021-11-11 15:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='имя отправителя')),
                ('email', models.EmailField(max_length=254, verbose_name='контактный е-майл')),
                ('message', models.TextField(verbose_name='сообщение')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время отправки')),
            ],
        ),
    ]
