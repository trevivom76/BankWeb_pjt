from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>', views.article_detail),
    path('<int:article_pk>/comment/', views.comment),  # 댓글 저장
    path('<int:article_pk>/comment/<int:comment_pk>', views.comment_detail)  # 댓글 삭제
    path('<int:article_pk>/likes/', views.likes),
]
