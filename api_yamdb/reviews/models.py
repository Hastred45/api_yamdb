from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


def get_delete_category():
    return Categories.objects.get_or_create(
        name='Категория была удалена администратором',
        slug='deleted'
    )[0]


class Categories(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.SlugField(unique=True,)


class Genres(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.SlugField(unique=True,)


class Title(models.Model):
    name = models.CharField(max_length=256,)
    year = models.IntegerField(default="",)
    description = models.CharField(max_length=256, blank=True, null=True)
    genre = models.ManyToManyField(
        Genres,
        related_name='genre',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET(get_delete_category()),
        related_name='category',
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_review',
        null=False,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_review',
        null=False,
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text

    class Meta:
        constraints = (
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_score_in_range_1_10",
                check=models.Q(score__gte=1) & models.Q(score__lt=11),
            ),
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='%(app_label)s_%(class)s_unique_title_author',
            ),
        )


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
