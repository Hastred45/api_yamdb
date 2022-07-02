import uuid

from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Categories, Genres, Review, Titles
from users.models import User

from .permissions import AnonReadOnlyAdminAll
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer, TokenSerializer)


@api_view(['POST'])
def signup_post(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user, create = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        return Response(
            'Такой логин или email уже существуют',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Код подверждения', confirmation_code,
        ['admin@email.com'], (email, ), fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token_post(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user_base = get_object_or_404(User, username=username)
    if confirmation_code == user_base.confirmation_code:
        token = str(AccessToken.for_user(user_base))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [AnonReadOnlyAdminAll]
    filter_backends = (filters.SearchFilter,)
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name', '=slug')
    lookup_field = 'slug'


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [AnonReadOnlyAdminAll]
    filter_backends = (filters.SearchFilter,)
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=name',)


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [AnonReadOnlyAdminAll]
    # filter_backends = (DjangoFilterBackend,)
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filterset_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    '''
    Отзывы.
    Вьюсет дает возможности:
    1. Получить список всех отзывов. Доступно без токена.
    2. Добавить новый отзыв. Пользователь может оставить
       только один отзыв на произведение.
       Доступно только аутентифицированным пользователям.
    3. Получить отзыв по id для указанного произведения. Доступно без токена.
    4. Частично обновить отзыв по id.
       Доступно только авторам отзыва, модераторам или администраторам.
    5. Удалить отзыв по id. Доступно только авторам отзыва,
       модераторам или администраторам.
    '''
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [AnonReadOnlyAdminAll]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title_u = get_object_or_404(Titles, pk=title_id)
        n_queryset = title_u.title_review.all()

        return n_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title_u = get_object_or_404(Titles, pk=title_id)
        serializer.save(author=self.request.user, title=title_u)


class CommentsViewSet(viewsets.ModelViewSet):
    '''
    Комментарии.
    Вьюсет дает возможности:
    1. Получить список всех комментариев к отзыву по id. Доступно без токена.
    2. Добавить новый комментарий для отзыва.
       Доступно только аутентифицированным пользователям.
    3. Получить комментарий для отзыва по id. Доступно без токена.
    4. Частично обновить комментарий к отзыву по id.
       Доступно только авторам комментария, модераторам или администраторам.
    5. Удалить комментарий к отзыву по id.
       Доступно только авторам комментария, модераторам или администраторам.
    '''
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [AnonReadOnlyAdminAll]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        review_id = self.kwargs.get("review_id")
        review_u = get_object_or_404(Review, pk=review_id, title=title)
        n_queryset = review_u.comment.all()
        return n_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        review_id = self.kwargs.get("review_id")
        review_u = get_object_or_404(Review, pk=review_id, title=title)
        serializer.save(author=self.request.user, review=review_u)
