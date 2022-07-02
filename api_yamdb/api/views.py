import uuid

from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
#from django_filters.rest_framework import DjangoFilterBackend надо разобраться с версиями Джанго
from rest_framework import mixins, status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticated

from reviews.models import Categories, Genres, Titles
from users.models import User
from .permissions import AnonReadOnlyAdminAll, OwnerOrAdmins
from .serializers import (CategoriesSerializer, GenresSerializer,
                          SignUpSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer, MeSerializer)


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrAdmins, )
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('username')
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [AnonReadOnlyAdminAll]
    filter_backends = (filters.SearchFilter,)
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
        

class GenresViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [AnonReadOnlyAdminAll]
    filter_backends = (filters.SearchFilter,)
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [AnonReadOnlyAdminAll]
    #filter_backends = (DjangoFilterBackend,)
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    #filterset_fields = ('category', 'genre', 'name', 'year')

    
class ReviewViewSet(viewsets.ModelViewSet):
    '''
    BLA BLA BLA
    Подписка.

    Все операции с подписками доступны только авторизованным
    пользователям.
    Вьюсет дает возможности:
    1. Получить список всех подписчиков автора запроса.
    2. Полученить, обновить, удалить подписку по id.
    Обновление, удаление подписок доступны только их
    авторам.
    '''
    pass
    # serializer_class = FollowSerializer
    # permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnly)
    # filter_backends = (filters.SearchFilter, )
    # search_fields = ('=following__username',)

    # def get_queryset(self):
    #     n_queryset = self.request.user.follower.all()
    #     return n_queryset

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class CommentsViewSet(viewsets.ModelViewSet):
    '''
    BLA BLA BLA
    Комментарии.

    Вьюсет дает возможности:
    1. Получить список всех комментариев.
    Добавление комментариев возможно только для авторизованных пользователей.
    2. Полученить, обновить, удалить комментария по id.
    Обновление, удаление комментария доступны только их авторам,
    анонимные запросы запрещены.
    '''
    pass
    # serializer_class = CommentSerializer
    # permission_classes = (OwnerOrReadOnly,)

    # def get_queryset(self):
    #     post_id = self.kwargs.get("post_id")
    #     post = get_object_or_404(Post, pk=post_id)
    #     n_queryset = post.comments.all()
    #     return n_queryset

    # def perform_create(self, serializer):
    #     post_id = self.kwargs.get("post_id")
    #     post = get_object_or_404(Post, pk=post_id)
    #     serializer.save(author=self.request.user, post=post)
