# Generated by Django 4.1.4 on 2023-01-06 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('description', models.CharField(max_length=1023)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flashcard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=63)),
                ('answer', models.CharField(max_length=63)),
                ('description', models.CharField(max_length=255)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.deck')),
            ],
        ),
        migrations.CreateModel(
            name='Holder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learned', models.IntegerField(default=0)),
                ('NumOfReviews', models.IntegerField(default=0)),
                ('LastReview', models.DateTimeField()),
                ('flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.flashcard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
