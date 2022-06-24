from django.urls import include, path
from rest_framework import routers

from .views import signup_post, token_post, ReviewViewSet, CommentsViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews',
)

router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentsViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', token_post),
    path('v1/auth/signup/', signup_post),
]
