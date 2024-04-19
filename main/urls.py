from django.urls import path
from .views import GetAllPosts, GetAllPostsCached, UpdatePost

urlpatterns = [
    path('posts/', GetAllPosts, name='get-all-posts'),
    path('post', GetAllPostsCached, name='get-post'),
    path('post/update', UpdatePost, name='update'),
]
