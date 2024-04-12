from django.urls import path
from .views import GetAllPosts, GetAllPostsCached

urlpatterns = [
    path('posts/', GetAllPosts, name='get-all-posts'),
    path('posts-cached/', GetAllPostsCached, name='get-all-posts'),
]
