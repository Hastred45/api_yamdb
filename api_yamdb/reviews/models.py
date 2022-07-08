from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import year_validator


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный человекочитаемый ключ для поиска категории'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный человекочитаемый ключ для поиска жанра'
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Имя произведения'
    )
    year = models.PositiveSmallIntegerField(
        default="",
        validators=[year_validator],
        verbose_name='Год произведения'
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'


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
