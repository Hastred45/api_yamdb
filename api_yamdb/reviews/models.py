from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


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
    genre = models.ManyToManyField(
        Genres,
        related_name='genre',
        #Тут вообще on_delete не бывает, я не хочу все переделывать на through модель
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING, #затык, надо разобраться
        related_name='category',
    )


class Review(models.Model):
    title = models.ForeignKey(
        User,
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


# TODODO обязательное поле ?? text


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review_comments',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
