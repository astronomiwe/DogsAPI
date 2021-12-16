# Generated by Django 3.2.8 on 2021-11-13 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_announcement_breed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breedinkennel',
            name='kennel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kennel_info', to='catalog.kennel', verbose_name='питомник'),
        ),
    ]
