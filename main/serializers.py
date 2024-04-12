from rest_framework import serializers
from .models import Post, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at']

