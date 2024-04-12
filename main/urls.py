from django.urls import path
from .views import GetAllPosts

urlpatterns = [
    path('posts/', GetAllPosts, name='get-all-posts'),
]
