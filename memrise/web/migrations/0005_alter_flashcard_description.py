# Generated by Django 4.0.6 on 2023-01-08 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_holder_needtoreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
