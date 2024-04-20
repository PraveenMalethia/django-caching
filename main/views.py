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
    posts = Post.objects.first()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def GetAllPostsCached(request):
    cached_post = cache.get("post")
    if cached_post is not None:
        return Response({"fetched_from_redis": cached_post})
    post = Post.objects.first()
    json_post = PostSerializer(post, many=False).data
    cache.set("post", json_post, timeout=15)
    return Response({"fetched_from_database": json_post})

@api_view(["INVALIDATE_AND_UPDATE","PUT"])
def UpdatePost(request):
    post = Post.objects.first()
    post.title = request.data.get('title',None)
    post.content = request.data.get('content',None)
    post.save()
    json_post = PostSerializer(post, many=False).data
    if request.method == 'INVALIDATE_AND_UPDATE':
        cache.delete("post")
        cache.set("post", json_post, timeout=15)
    return Response({"post": json_post})

