# Generated by Django 2.2.16 on 2022-06-26 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_genres'),
    ]

    operations = [
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256)),
                ('year', models.IntegerField(default='')),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='reviews.Categories')),
                ('genre', models.ManyToManyField(related_name='genre', to='reviews.Genres')),
            ],
        ),
    ]
