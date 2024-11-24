from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import *


# 사용자 정보
# @csrf_exempt
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_info(request, username):
    if request.user.username == username:
        if request.method == 'GET':
            user = get_object_or_404(get_user_model(), username=username)
            serializer = UserInfoSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PUT':
            user = get_object_or_404(get_user_model(), username=username)
            serializer = UserInfoSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사용자 프로필 정보
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    if request.user.username == username:
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)


# 사용자 프로필 사진 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_img(request, username):
    if request.user.username == username:
        if request.method == 'PUT':
            user = get_object_or_404(get_user_model(), username=username)
            data = { 'profile_img': request.data['profile_img[]']}
            serializer = UserInfoSerializer(instance=user, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)