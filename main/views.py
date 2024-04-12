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
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    cached_posts = cache.get("posts")
    if cached_posts is not None:
        return Response({"fetched_from_redis": cached_posts})
    cache.set("posts", serializer.data, timeout=30)
    return Response({"fetched_from_database": serializer.data})
