from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, 'categories')

urlpatterns = [
    path('v1/', include(router.urls))
]