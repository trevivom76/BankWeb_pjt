from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, get_list_or_404
from articles.models import *
from articles.serializers import *


# 전체 게시글 목록 조회
@api_view(['GET'])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True, context={'request': request})  # context 전달
        return Response(serializer.data)


# 게시글 작성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_article(request):
    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data, context={'request': request})  # context 전달
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 단일 게시글 조회, 수정, 삭제
@api_view(['GET','PUT','DELETE'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, id=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article, context={'request': request})  # context 전달
        return Response(serializer.data)
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            serializer = ArticleSerializer(article, data=request.data, partial=True, context={'request': request})  # context 전달
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({ "detail": "Authentication credentials were not provided." }, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            if request.user == article.user:
                article.delete()
            return Response({ "detail": f'{article_pk}번의 게시글이 삭제되었습니다.' }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "detail": "Authentication credentials were not provided." }, status=status.HTTP_401_UNAUTHORIZED)


# 댓글 조회
@api_view(['GET'])
def comment_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


# 댓글 작성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 수정, 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            comment.delete()
            return Response({ "detail": f'{article_pk}번 게시글의 {comment_pk}번의 댓글이 삭제되었습니다.' }, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({ "detail": "Authentication credentials were not provided." }, status=status.HTTP_401_UNAUTHORIZED)
        