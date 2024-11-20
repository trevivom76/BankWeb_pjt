from dataclasses import fields
from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

# 사용자 정보
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'profile_img', 'nickname')


# 게시글 목록
class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'title', 'user', 'category')


# 게시글 세부 정보
class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'


# 댓글 목록
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)