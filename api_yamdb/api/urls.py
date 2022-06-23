from django.urls import path

from .views import signup_post, token_post

app_name = 'api'

urlpatterns = [
    path('v1/auth/token/', token_post),
    path('v1/auth/signup/', signup_post)
]
