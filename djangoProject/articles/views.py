from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from articles.models import *


# Create your views here.
def article_list(request):
    if request.method == 'GET':
        articles = get_object_or_404(Article)
        serializer = UserInfoSerializer(articles)
        return Response(serializer.data)