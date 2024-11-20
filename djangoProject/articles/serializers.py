from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

# 사용자 정보
class UserSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'nickname', 'profile_img')

    def get_profile_img(self, obj):
        request = self.context.get('request')
        if obj.profile_img:
            # 절대 URL 생성
            return request.build_absolute_uri(obj.profile_img.url)
        return None


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