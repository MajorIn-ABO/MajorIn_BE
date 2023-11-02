from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.user_view, name='user'),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/users/create/', views.UserCreate.as_view(), name='user-create'),
    path('api/users/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    
    path('api/boards/posts/', views.BoardList.as_view(), name='board-list'),
    path('api/boards/posts/<int:pk>/', views.BoardDetail.as_view(), name='board-detail'),
    path('api/boards/posts-by-category/<str:category_id>/', views.BoardListByCategory.as_view(), name='board-list-by-category'),
    path('api/boards/posts/create/', views.BoardCreate.as_view(), name='board-create'),
    path('api/boards/posts/<int:pk>/update/', views.BoardUpdate.as_view(), name='board-update'),
    path('api/boards/posts/<int:pk>/delete/', views.BoardDelete.as_view(), name='board-delete'),
    
    path('api/boards/posts/comments/', views.BoardCommentList.as_view(), name='board-comment-list'),
    path('api/boards/posts/comments/<int:pk>/', views.BoardCommentDetail.as_view(), name='board-comment-detail'),
    path('api/boards/posts/comments-by-parent/<str:parent_comment>/', views.BoardCommentListByParent.as_view(), name='board-comment-list-by-parent'),
    path('api/boards/posts/comments/create/', views.BoardCommentCreate.as_view(), name='board-comment-create'),
    path('api/boards/posts/comments/<int:pk>/update/', views.BoardCommentUpdate.as_view(), name='board-comment-update'),
    path('api/boards/posts/comments/<int:pk>/delete/', views.BoardCommentDelete.as_view(), name='board-comment-delete'),
]
