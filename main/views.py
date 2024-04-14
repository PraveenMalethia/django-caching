from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
# from rest_framework import status
from django.core.cache import cache
from .models import Post
from .serializers import PostSerializer


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


@api_view(["GET"])
def GetAllPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def GetAllPostsCached(request):
    cached_posts = cache.get("posts")
    if cached_posts is not None:
        return Response({"fetched_from_redis": cached_posts})
    posts = Post.objects.all()
    json_posts = PostSerializer(posts, many=True).data
    cache.set("posts", json_posts, timeout=15)
    return Response({"fetched_from_database": json_posts})
