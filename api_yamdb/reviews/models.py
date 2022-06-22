from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.CharField(max_length=256, blank=True, null=True)
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name='genre',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='category'
    )
