from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list),  # 전체 게시글 목록 조회(GET)
    path('create/', views.create_article),  # 게시글 작성(POST)
    path('<int:article_pk>', views.article_detail), # 단일 게시글 조회 및 수정, 삭제(GET, PUT, DELETE)
    path('<int:article_pk>/create_comment/', views.create_comment),  # 댓글 작성(POST)
    path('<int:article_pk>/commnet_list/', views.commnet_list),  # 댓글 목록 조회(GET)
    path('<int:article_pk>/comment/<int:comment_pk>', views.comment_detail),  # 댓글 삭제, 수정(PUT, DELETE)
    path('<int:article_pk>/likes/', views.likes),
]