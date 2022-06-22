from rest_framework import viewsets
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from reviews.models import Categories, Genres, Titles
from .serializers import CategoriesSerializer

class CategoriesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    # работа в процессе
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Categories, slug=self.kwargs)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
        