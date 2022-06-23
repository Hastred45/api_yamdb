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


# class Reviews(models.Model):
#     text = models.TextField()
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='posts')
#     pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    
#     image = models.ImageField(
#         upload_to='posts/', null=True, blank=True)
#     group = models.ForeignKey(
#         Group, on_delete=models.CASCADE,
#         related_name="posts", blank=True, null=True
#     )

#     def __str__(self):
#         return self.text

# class Comment(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments')
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='comments')
#     text = models.TextField()
#     created = models.DateTimeField(
#         'Дата добавления', auto_now_add=True, db_index=True)
