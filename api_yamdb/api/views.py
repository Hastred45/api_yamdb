from rest_framework import viewsets
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from reviews.models import Categories, Genres, Titles
from .serializers import CategoriesSerializer, GenresSerializer, TitleSerializer

class CategoriesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
        

class GenresViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):

    queryset = Titles.objects.all()
    serializer_class = TitleSerializer