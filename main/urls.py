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
    path('api/boards/posts-by-userid/<int:user_id>/', views.BoardListByUserId.as_view(), name='board-list-by-userid'),
    path('api/boards/posts-by-category/<str:category_id>/', views.BoardListByCategory.as_view(), name='board-list-by-category'),
    path('api/boards/posts/create/', views.BoardCreate.as_view(), name='board-create'),
    path('api/boards/posts/<int:pk>/update/', views.BoardUpdate.as_view(), name='board-update'),
    path('api/boards/posts/<int:pk>/delete/', views.BoardDelete.as_view(), name='board-delete'),
    
    path('api/boards/posts/comments/', views.BoardCommentList.as_view(), name='board-comment-list'),
    path('api/boards/posts/comments/<int:pk>/', views.BoardCommentDetail.as_view(), name='board-comment-detail'),
    path('api/boards/posts/comments-by-userid/<int:user_id>/', views.BoardCommentListByUserId.as_view(), name='board-comment-list-by-userid'),
    path('api/boards/posts/comments-by-postid/<int:post_id>/', views.BoardCommentListByPostId.as_view(), name='board-comment-list-by-postid'),
    path('api/boards/posts/comments-by-parent/<int:parent_comment>/', views.BoardCommentListByParent.as_view(), name='board-comment-list-by-parent'),
    #path('api/boards/posts/comments/<int:post_id>/<int:user_id>/create/', views.BoardCommentCreate.as_view(), name='board-comment-create'),
    path('api/boards/posts/comments/create/', views.BoardCommentCreate.as_view(), name='board-comment-create'),
    path('api/boards/posts/comments/<int:pk>/update/', views.BoardCommentUpdate.as_view(), name='board-comment-update'),
    path('api/boards/posts/comments/<int:pk>/delete/', views.BoardCommentDelete.as_view(), name='board-comment-delete'),

    path('api/boards/posts/likes/', views.BoardLikeList.as_view(), name='board-like-list'),
    path('api/boards/posts/likes-by-userid/<int:user_id>/', views.BoardLikeListByUserId.as_view(), name='board-like-list-by-userid'),
    path('api/boards/posts/likes-by-postid/<int:post_id>/', views.BoardLikeListByPostId.as_view(), name='board-like-list-by-postid'),
    path('api/boards/posts/likes/<int:post_id>/<int:user_id>/create/', views.BoardLikeCreate.as_view(), name='board-like-create'),

    path('api/boards/posts/bookmarks/', views.BoardBookmarkList.as_view(), name='board-bookmark-list'),
    path('api/boards/posts/bookmarks-by-userid/<int:user_id>/', views.BoardBookmarkListByUserId.as_view(), name='board-bookmark-list-by-userid'),
    path('api/boards/posts/bookmarks-by-postid/<int:post_id>/', views.BoardBookmarkListByPostId.as_view(), name='board-bookmark-list-by-postid'),
    path('api/boards/posts/bookmarks/<int:post_id>/<int:user_id>/create/', views.BoardBookmarkCreate.as_view(), name='board-bookmark-create'),

    path('api/studys/posts/', views.StudyList.as_view(), name='study-list'),
    path('api/studys/posts/<int:pk>/', views.StudyDetail.as_view(), name='study-detail'),
    path('api/studys/posts-by-userid/<int:user_id>/', views.StudyListByUserId.as_view(), name='study-list-by-userid'),
    path('api/studys/posts/create/', views.StudyCreate.as_view(), name='study-create'),
    path('api/studys/posts/<int:pk>/update/', views.StudyUpdate.as_view(), name='study-update'),
    path('api/studys/posts/<int:pk>/delete/', views.StudyDelete.as_view(), name='study-delete'),

    path('api/studys/posts/comments/', views.StudyCommentList.as_view(), name='study-comment-list'),
    path('api/studys/posts/comments/<int:pk>/', views.StudyCommentDetail.as_view(), name='study-comment-detail'),
    path('api/studys/posts/comments-by-userid/<int:user_id>/', views.StudyCommentListByUserId.as_view(), name='study-comment-list-by-userid'),
    path('api/studys/posts/comments-by-postid/<int:studypost_id>/', views.StudyCommentListByPostId.as_view(), name='study-comment-list-by-postid'),
    path('api/studys/posts/comments-by-parent/<int:parent_comment>/', views.StudyCommentListByParent.as_view(), name='study-comment-list-by-parent'),
    path('api/studys/posts/comments/create/', views.StudyCommentCreate.as_view(), name='study-comment-create'),
    path('api/studys/posts/comments/<int:pk>/update/', views.StudyCommentUpdate.as_view(), name='study-comment-update'),
    path('api/studys/posts/comments/<int:pk>/delete/', views.StudyCommentDelete.as_view(), name='study-comment-delete'),

    path('api/studys/posts/likes/', views.StudyLikeList.as_view(), name='study-like-list'),
    path('api/studys/posts/likes-by-userid/<int:user_id>/', views.StudyLikeListByUserId.as_view(), name='study-like-list-by-userid'),
    path('api/studys/posts/likes-by-postid/<int:studypost_id>/', views.StudyLikeListByPostId.as_view(), name='study-like-list-by-postid'),
    path('api/studys/posts/likes/<int:post_id>/<int:user_id>/create/', views.StudyLikeCreate.as_view(), name='study-like-create'),

    path('api/usedbooktrades/book/search/', views.BookSearchAPIView.as_view(), name='book-search-api'),

    path('api/usedbooktrades/posts/', views.UsedbooktradeList.as_view(), name='usedbooktrade-list'),
    path('api/usedbooktrades/posts/<int:pk>/', views.UsedbooktradeDetail.as_view(), name='usedbooktrade-detail'),
    path('api/usedbooktrades/posts-by-userid/<int:user_id>/', views.UsedbooktradeListByUserId.as_view(), name='usedbooktrade-list-by-userid'),
    path('api/usedbooktrades/posts/create/', views.UsedbooktradeCreate.as_view(), name='usedbooktrade-create'),
    path('api/usedbooktrades/posts/<int:pk>/update/', views.UsedbooktradeUpdate.as_view(), name='usedbooktrade-update'),
    path('api/usedbooktrades/posts/<int:pk>/delete/', views.UsedbooktradeDelete.as_view(), name='usedbooktrade-delete'),

    path('api/usedbooktrades/posts/comments/', views.UsedbooktradeCommentList.as_view(), name='usedbooktrade-comment-list'),
    path('api/usedbooktrades/posts/comments/<int:pk>/', views.UsedbooktradeCommentDetail.as_view(), name='usedbooktrade-comment-detail'),
    path('api/usedbooktrades/posts/comments-by-userid/<int:user_id>/', views.UsedbooktradeCommentListByUserId.as_view(), name='usedbooktrade-comment-list-by-userid'),
    path('api/usedbooktrades/posts/comments-by-postid/<int:Usedbookpost_id>/', views.UsedbooktradeCommentListByPostId.as_view(), name='usedbooktrade-comment-list-by-postid'),
    path('api/usedbooktrades/posts/comments-by-parent/<int:parent_comment>/', views.UsedbooktradeCommentListByParent.as_view(), name='usedbooktrade-comment-list-by-parent'),
    path('api/usedbooktrades/posts/comments/create/', views.UsedbooktradeCommentCreate.as_view(), name='usedbooktrade-comment-create'),
    path('api/usedbooktrades/posts/comments/<int:pk>/update/', views.UsedbooktradeCommentUpdate.as_view(), name='usedbooktrade-comment-update'),
    path('api/usedbooktrades/posts/comments/<int:pk>/delete/', views.UsedbooktradeCommentDelete.as_view(), name='usedbooktrade-comment-delete'),
]
