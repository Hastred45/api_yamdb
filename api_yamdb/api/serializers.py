from rest_framework import serializers
# ,Review
from rest_framework.response import Response

from reviews.models import Categories, Genres, Titles


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Нельзя использовать логин me')
        return data

    class Meta:
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')

     
class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Categories
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genres
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles


# class ReviewSerializer(serializers.ModelSerializer):

#     author = serializers.SlugRelatedField(
#         read_only=True,
#         default=serializers.CurrentUserDefault(),
#         slug_field="username"
#     )

#     class Meta:
#         model = Review
#         fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
#         read_only_fields = ('id', 'title', 'author', 'pub_date')

    # def create(self, validated_data):
    #     if 'group' not in self.initial_data:
    #         post = Post.objects.create(**validated_data)
    #     else:
    #         group = validated_data.pop('group')
    #         current_group, status = Group.objects.filter(
    #             id=group.id
    #         ).get_or_create(group)
    #         post = Post.objects.create(**validated_data, group=current_group)

    #     return post


# class Review(models.Model):
#     title = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='title_review',
#         null=False,
#     )
#     text = models.TextField()
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='author_review',
#         null=False,
#     )
#     score = models.IntegerField(
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(10),
#         ]
#     )
#     pub_date = models.DateTimeField(
#         'Дата публикации',
#         auto_now_add=True
#     )

  

#     class Meta:
#         constraints = (
#             models.CheckConstraint(
#                 name="%(app_label)s_%(class)s_score_in_range_1_10",
#                 check=models.Q(score__gte=1) & models.Q(score__lt=11),
#             ),
#             models.UniqueConstraint(
#                 fields=('title', 'author'),
#                 name='%(app_label)s_%(class)s_unique_title_author',
#             ),
#         )


# # TODODO обязательное поле ?? text


# class Comments(models.Model):
#     review = models.ForeignKey(
#         Review,
#         on_delete=models.CASCADE,
#         related_name='review_comments',
#     )
#     text = models.TextField()
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='author_comments',
#     )
#     pub_date = models.DateTimeField(
#         'Дата публикации',
#         auto_now_add=True,
#     )
