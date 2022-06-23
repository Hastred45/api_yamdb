from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, 'categories')
router.register('genres', GenresViewSet, 'genres')
router.register('titles', TitlesViewSet, 'titles')

urlpatterns = [
    path('v1/', include(router.urls))
]