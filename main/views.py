from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone  # 필요한 경우 추가
from django.http import JsonResponse
from .models import User, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like, Usedbooktrade, UsedbooktradeData, Usedbooktrade_Comment
from .serializers import UserSerializer, BoardSerializer, BoardCommentSerializer, BoardLikeSerializer, BoardBookmarkSerializer, StudySerializer, StudyCommentSerializer, StudyLikeSerializer, UsedbooktradeSerializer, UsedbooktradeDataSerializer, UsedbooktradeCommentSerializer
import json
import requests
from dotenv import load_dotenv
import os 

# load .env
load_dotenv()

NAVER_Client_ID = os.environ.get('Client_ID')
NAVER_Client_Secret = os.environ.get('Client_Secret')


# 유저 관련 API 모음
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 게시글 관련 API 모음

class BoardList(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardListByUserId(generics.ListAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board.objects.filter(user_id=user_id)
    
class BoardListByCategory(generics.ListAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Board.objects.filter(category_id=category_id)

class BoardDetail(generics.RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardCreate(generics.CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardUpdate(generics.UpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDelete(generics.DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# 게시글 댓글 관련 API 모음

class BoardCommentList(generics.ListAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

class BoardCommentListByUserId(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board_Comment.objects.filter(user_id=user_id)
    
class BoardCommentListByPostId(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Board_Comment.objects.filter(post_id=post_id)

class BoardCommentListByParent(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Board_Comment.objects.filter(parent_comment=parent_comment)

class BoardCommentDetail(generics.RetrieveAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

class BoardCommentCreate(generics.CreateAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer = BoardCommentSerializer(data=request.data)

        if serializer.is_valid():
            # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
            # user = request.user

            user_id = serializer.validated_data["user_id"].id
            post_id = serializer.validated_data["post_id"].id
            contents = serializer.validated_data["contents"]
            
            try:
                board_post = Board.objects.get(pk=post_id)
            except Board.DoesNotExist:
                return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)

            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # serializer.save()  # 댓글을 저장하고
        
            comment = Board_Comment(user_id=user, post_id=board_post, contents=contents)
            comment.save()

            board_post.comment += 1
            board_post.save(update_fields=['comment'])
            return Response({"message": "Comment created successfully.", "comments": board_post.comment}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardCommentUpdate(generics.UpdateAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

class BoardCommentDelete(generics.DestroyAPIView):
    queryset = Board_Comment.objects.all()

    def destroy(self, request, *args, **kwargs):

        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user

        # user_id = request.data.get("user_id")
        # post_id = request.data.get("post_id")
        comment_id = kwargs.get("pk")  # pk는 URL에서 가져온 댓글의 기본 키 값
        
        try:
            board_comment = Board_Comment.objects.get(pk=comment_id)
        except Board_Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        '''
        # 댓글을 작성한 사용자와 요청한 사용자가 일치하는지 확인
        if user_id != board_comment.user_id.id:
            return Response({"error": "Unauthorized. You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        # 댓글이 속한 게시물과 요청한 게시물이 일치하는지 확인
        if post_id != board_comment.post_id.id:
            return Response({"error": "Invalid request. The comment does not belong to the specified post."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        '''

        board_comment.delete()

        # 게시물의 댓글 수 업데이트
        try:
            board_post = Board.objects.get(pk=board_comment.post_id.id)
        except Board.DoesNotExist:
            return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)

        board_post.comment -= 1
        board_post.save(update_fields=['comment'])

        return Response({"message": "Comment deleted successfully.", "comments": board_post.comment}, status=status.HTTP_204_NO_CONTENT)

# 게시글 좋아요 관련 API

class BoardLikeList(generics.ListAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardLikeSerializer

class BoardLikeListByUserId(generics.ListAPIView):
    serializer_class = BoardLikeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board_Like.objects.filter(user_id=user_id)
    
class BoardLikeListByPostId(generics.ListAPIView):
    serializer_class = BoardLikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Board_Like.objects.filter(post_id=post_id)

class BoardLikeCreate(APIView):
    
    def post(self, request, post_id, user_id):
        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user
        try:
            board_post = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 좋아요를 이미 눌렀는지 확인
        is_liked = Board_Like.objects.filter(user_id=user, post_id=board_post).exists()

        if is_liked:
            # 이미 좋아요를 누른 경우 좋아요를 취소
            like = Board_Like.objects.get(user_id=user, post_id=board_post)
            like.delete()
            # like.delete_date = timezone.now()  # delete_date 필드에 현재 시간 설정
            # like.save()
            board_post.like -= 1
            board_post.save(update_fields=['like'])
            return Response({"message": "Like removed successfully.", "likes": board_post.like}, status=status.HTTP_200_OK)
        else:
            # 좋아요를 누르지 않은 경우 좋아요 추가
            like = Board_Like(user_id=user, post_id=board_post)
            like.save()
            board_post.like += 1
            board_post.save(update_fields=['like'])
            return Response({"message": "Like created successfully.", "likes": board_post.like}, status=status.HTTP_201_CREATED)

# 게시글 북마크 관련 API

class BoardBookmarkList(generics.ListAPIView):
    queryset = Board_bookmark.objects.all()
    serializer_class = BoardBookmarkSerializer

class BoardBookmarkListByUserId(generics.ListAPIView):
    serializer_class = BoardBookmarkSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board_bookmark.objects.filter(user_id=user_id)
    
class BoardBookmarkListByPostId(generics.ListAPIView):
    serializer_class = BoardBookmarkSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Board_bookmark.objects.filter(post_id=post_id)

class BoardBookmarkCreate(APIView):
    
    def post(self, request, post_id, user_id):
        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user
        try:
            board_post = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 북마크를 이미 눌렀는지 확인
        is_kept = Board_bookmark.objects.filter(user_id=user, post_id=board_post).exists()

        if is_kept:
            # 이미 북마크를 누른 경우 북마크를 취소
            keep = Board_bookmark.objects.get(user_id=user, post_id=board_post)
            keep.delete()
            # keep.delete_date = timezone.now()  # delete_date 필드에 현재 시간 설정
            # keep.save()
            board_post.keep -= 1
            board_post.save(update_fields=['keep'])
            return Response({"message": "keep removed successfully.", "keeps": board_post.keep}, status=status.HTTP_200_OK)
        else:
            # 북마크를 누르지 않은 경우 북마크 추가
            keep = Board_bookmark(user_id=user, post_id=board_post)
            keep.save()
            board_post.keep += 1
            board_post.save(update_fields=['keep'])
            return Response({"message": "Keep created successfully.", "keeps": board_post.keep}, status=status.HTTP_201_CREATED)
    
# 스터디 관련 API 모음

class StudyList(generics.ListAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class StudyListByUserId(generics.ListAPIView):
    serializer_class = StudySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study.objects.filter(user_id=user_id)

class StudyDetail(generics.RetrieveAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class StudyCreate(generics.CreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudyUpdate(generics.UpdateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class StudyDelete(generics.DestroyAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer


# 스터디 댓글 관련 API 모음

class StudyCommentList(generics.ListAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

class StudyCommentListByUserId(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study_Comment.objects.filter(user_id=user_id)
    
class StudyCommentListByPostId(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        studypost_id = self.kwargs['studypost_id']
        return Study_Comment.objects.filter(studypost_id=studypost_id)

class StudyCommentListByParent(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Study_Comment.objects.filter(parent_comment=parent_comment)

class StudyCommentDetail(generics.RetrieveAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

class StudyCommentCreate(generics.CreateAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer = StudyCommentSerializer(data=request.data)

        if serializer.is_valid():
            # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
            # user = request.user

            user_id = serializer.validated_data["user_id"].id
            studypost_id = serializer.validated_data["studypost_id"].id
            contents = serializer.validated_data["contents"]
            
            try:
                study_post = Study.objects.get(pk=studypost_id)
            except Study.DoesNotExist:
                return Response({"error": "Study post not found."}, status=status.HTTP_404_NOT_FOUND)

            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # serializer.save()  # 댓글을 저장하고
        
            comment = Study_Comment(user_id=user, studypost_id=study_post, contents=contents)
            comment.save()

            study_post.comment += 1
            study_post.save(update_fields=['comment'])
            return Response({"message": "Comment created successfully.", "comments": study_post.comment}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudyCommentUpdate(generics.UpdateAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

class StudyCommentDelete(generics.DestroyAPIView):
    queryset = Study_Comment.objects.all()

    def destroy(self, request, *args, **kwargs):

        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user

        # user_id = request.data.get("user_id")
        # studypost_id = request.data.get("studypost_id")
        comment_id = kwargs.get("pk")  # pk는 URL에서 가져온 댓글의 기본 키 값
        
        try:
            study_comment = Study_Comment.objects.get(pk=comment_id)
        except Study_Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        '''
        # 댓글을 작성한 사용자와 요청한 사용자가 일치하는지 확인
        if user_id != study_comment.user_id.id:
            return Response({"error": "Unauthorized. You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        # 댓글이 속한 스터디 게시물과 요청한 스터디 게시물이 일치하는지 확인
        if studypost_id != study_comment.studypost_id.id:
            return Response({"error": "Invalid request. The comment does not belong to the specified post."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        '''

        study_comment.delete()

        # 스터디 게시물의 댓글 수 업데이트
        try:
            study_post = Study.objects.get(pk=study_comment.studypost_id.id)
        except Study.DoesNotExist:
            return Response({"error": "Study post not found."}, status=status.HTTP_404_NOT_FOUND)

        study_post.comment -= 1
        study_post.save(update_fields=['comment'])

        return Response({"message": "Comment deleted successfully.", "comments": study_post.comment}, status=status.HTTP_204_NO_CONTENT)


# 스터디 좋아요 관련 API

class StudyLikeList(generics.ListAPIView):
    queryset = Study_Like.objects.all()
    serializer_class = StudyLikeSerializer

class StudyLikeListByUserId(generics.ListAPIView):
    serializer_class = StudyLikeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study_Like.objects.filter(user_id=user_id)
    
class StudyLikeListByPostId(generics.ListAPIView):
    serializer_class = StudyLikeSerializer

    def get_queryset(self):
        studypost_id = self.kwargs['studypost_id']
        return Study_Like.objects.filter(studypost_id=studypost_id)

class StudyLikeCreate(APIView):
    
    def post(self, request, post_id, user_id):
        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user
        try:
            study_post = Study.objects.get(pk=post_id)
        except Study.DoesNotExist:
            return Response({"error": "Study post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 좋아요를 이미 눌렀는지 확인
        is_liked = Study_Like.objects.filter(user_id=user, studypost_id=study_post).exists()

        if is_liked:
            # 이미 좋아요를 누른 경우 좋아요를 취소
            like = Study_Like.objects.get(user_id=user, studypost_id=study_post)
            like.delete()
            # like.delete_date = timezone.now()  # delete_date 필드에 현재 시간 설정
            # like.save()
            study_post.like -= 1
            study_post.save(update_fields=['like'])
            return Response({"message": "Like removed.", "likes": study_post.like}, status=status.HTTP_200_OK)
        else:
            # 좋아요를 누르지 않은 경우 좋아요 추가
            like = Study_Like(user_id=user, studypost_id=study_post)
            like.save()
            study_post.like += 1
            study_post.save(update_fields=['like'])
            return Response({"message": "Liked.", "likes": study_post.like}, status=status.HTTP_201_CREATED)


# 중고거래 관련 API 모음

class UsedbooktradeList(generics.ListAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer

class UsedbooktradeListByUserId(generics.ListAPIView):
    serializer_class = UsedbooktradeSerializer

    def get_queryset(self):
        seller_id = self.kwargs['seller']
        return Usedbooktrade.objects.filter(seller=seller_id)

class UsedbooktradeDetail(generics.RetrieveAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer


# 중고거래 글 작성

@method_decorator(csrf_exempt, name='dispatch')
class UsedbooktradeCreate(generics.CreateAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        try:
            # 유저 입력 데이터 추출
            seller = request.data.get('seller')
            sell_price = request.data.get('price')
            # imgfile = request.data.get('imgfile')
            description = request.data.get('description')
            damage_level = request.data.get('damage_level')

            book_title = "운영체제"
            book_data = search_books_by_title(book_title, NAVER_Client_ID, NAVER_Client_Secret)

            # DB에 저장
            usedbooktrade_data = {
                'title': book_data['items'][0].get('title', ''),
                'author': book_data['items'][0].get('author', ''),
                'seller': seller,
                'publisher': book_data['items'][0].get('publisher', ''),
                'price': sell_price,
                'imgfile': book_data['items'][0].get('image', ''),
                'description': description,
                'damage_level': damage_level,
            }

            try:
                user = User.objects.get(pk=seller)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # 모델 인스턴스 생성
            usedbooktrade_instance = Usedbooktrade(
                title=usedbooktrade_data['title'],
                author=usedbooktrade_data['author'],
                seller=user,
                publisher=usedbooktrade_data['publisher'],
                price=usedbooktrade_data['price'],
                imgfile=usedbooktrade_data['imgfile'],
                description=usedbooktrade_data['description'],
                damage_level=usedbooktrade_data['damage_level'],
            )

            # 모델 인스턴스 저장
            usedbooktrade_instance.save()

            # 저장된 인스턴스의 ID 반환 (옵션)
            # Usedbooktrade_post = Usedbooktrade.objects.get(pk=usedbooktrade_instance.id)

            return Response({"message": "Usedbooktrade post created successfully.", "results": usedbooktrade_data}, status=status.HTTP_201_CREATED)

            '''
            serializer = UsedbooktradeSerializer(data=usedbooktrade_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            '''
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class SaveUsedBookAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            # POST 요청에서 중고도서 정보 추출
            title = request.POST.get('title')
            author = request.POST.get('author')
            seller = request.POST.get('seller')
            publisher = request.POST.get('publisher')
            price = request.POST.get('sell_price')
            imgfile = request.POST.get('imgfile')
            description = request.POST.get('description')
            damage_level = request.POST.get('damage_level')
            # 이미지 파일 처리 등 추가 코드 작성 필요

            try:
                user = User.objects.get(pk=seller)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # 중고도서 정보 저장
            used_book = Usedbooktrade.objects.create(
                title=title,
                author=author,
                seller=user,
                publisher=publisher,
                price=price,
                imgfile=imgfile,
                description=description,
                damage_level=damage_level,
                # 필요한 다른 필드들도 추가할 수 있습니다.
            )
            
            return JsonResponse({'success': True, 'message': '중고도서 정보가 성공적으로 저장되었습니다.'})
        
        except Exception as e:
            # 예외 처리
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        

class UsedbooktradeUpdate(generics.UpdateAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer

class UsedbooktradeDelete(generics.DestroyAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer


# 데이터 임시 저장을 위한 클래스 

class SharedBookInfo:
    cached_book_info = {}

# 중고거래 도서 검색 API
# http://127.0.0.1:8000/api/usedbooktrades/book/search/?book_title=검색어

@method_decorator(csrf_exempt, name='dispatch')
class BookSearchAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user
        try:
            # GET 요청에서 도서 이름 추출
            book_title = request.GET.get('book_title', '')

            book_data = search_books_by_title(book_title, NAVER_Client_ID, NAVER_Client_Secret)
            print(book_data)

            # 결과가 있는지 확인
            if 'items' in book_data and book_data['items']:
                # 검색 결과 반환
                # 전체 도서 정보를 클래스 변수에 저장
                SharedBookInfo.cached_book_info[book_title] = {
                    'title': book_data['items'][0].get('title', ''),
                    'author': book_data['items'][0].get('author', ''),
                    'publisher': book_data['items'][0].get('publisher', ''),
                    'price': book_data['items'][0].get('discount', ''),
                    'imgfile': book_data['items'][0].get('image', ''),
                }

                return render(request, 'main/book_search_result.html', {'book_data_list': book_data['items']})
                
                # return JsonResponse(SharedBookInfo.cached_book_info[book_title])
                # return JsonResponse({'success': True, 'data': book_data['items'][0]})
            else:
                # 검색 결과가 없을 경우
                return JsonResponse({'success': False, 'message': '도서를 찾을 수 없습니다.'}, status=404)
                # return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
              
        except Exception as e:
            # 예외 처리
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        

# 네이버 API 사용 외부 데이터 가져오는 코드

def search_books_by_title(book_title, client_id, client_secret):
    # 네이버 도서 검색 API 엔드포인트
    naver_api_url = f'https://openapi.naver.com/v1/search/book.json'

    # API에 전송할 파라미터 설정
    params = {'query': book_title, 'display': 15}

    # 네이버 API 요청에 필요한 헤더 설정
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

    # API 요청 보내기
    response = requests.get(naver_api_url, params=params, headers=headers)

    # 응답 확인
    if response.status_code == 200:
        # JSON 형태로 반환된 응답 데이터를 파이썬 딕셔너리로 변환
        
        return response.json()

    else:
        # API 요청이 실패한 경우 에러 코드 출력
        return JsonResponse({'success': False, 'message': f'API 요청 실패 - 상태 코드: {response.status_code}'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class BookSelectAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            # POST 요청에서 선택된 도서의 정보 추출
            title = request.POST.get('title')
            author = request.POST.get('author')
            publisher = request.POST.get('publisher')
            price = request.POST.get('price')
            imgfile = request.POST.get('imgfile')
            
            # 받은 정보를 JSON 형태로 응답
            book_info = {
                'title': title,
                'author': author,
                'publisher': publisher,
                'price': price,
                'imgfile': imgfile,
                # 필요한 다른 정보들을 추가할 수 있습니다.
            }
            
            return render(request, 'main/book_post.html', {'book_info': book_info})
        
        except Exception as e:
            # 예외 처리
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 중고거래 거래내역 관련 API 모음

class UsedbooktradeSold(APIView):
    def post(self, request, usedbooktrade_id):
        # 해당 책 모델 조회
        usedbooktrade = get_object_or_404(Usedbooktrade, id=usedbooktrade_id)

        # 판매자 확인 (현재 로그인한 사용자를 판매자로 설정)
        # seller = request.user

        seller = usedbooktrade.seller

        print(seller)
        print(usedbooktrade.is_sold)

        # 책이 판매되지 않았다면
        if usedbooktrade.is_sold:
            # is_sold 컬럼을 True로 업데이트
            usedbooktrade.is_sold = True
            usedbooktrade.save()

            # UsedbooktradeData에 판매된 책 데이터 등록
            UsedbooktradeData.objects.create(trade=usedbooktrade, sellerid=seller)

            return Response({"message": "책이 성공적으로 판매되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "이미 판매된 책입니다."}, status=status.HTTP_400_BAD_REQUEST)

class UsedbooktradedataList(generics.ListAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

class UsedbooktradedataListByTradeId(generics.ListAPIView):
    serializer_class = UsedbooktradeDataSerializer

    def get_queryset(self):
        trade_id = self.kwargs['trade']
        return UsedbooktradeData.objects.filter(trade=trade_id)
    
class UsedbooktradedataListBySellerId(generics.ListAPIView):
    serializer_class = UsedbooktradeDataSerializer

    def get_queryset(self):
        sellerid = self.kwargs['sellerid']
        return UsedbooktradeData.objects.filter(sellerid=sellerid)

class UsedbooktradedataDetail(generics.RetrieveAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

'''
class UsedbooktradedataCreate(generics.CreateAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

class UsedbooktradedataUpdate(generics.UpdateAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

class UsedbooktradedataDelete(generics.DestroyAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer





# 중고거래 댓글 관련 API 모음

class UsedbooktradeCommentList(generics.ListAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

class UsedbooktradeCommentListByUserId(generics.ListAPIView):
    serializer_class = UsedbooktradeCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Usedbooktrade_Comment.objects.filter(user_id=user_id)
    
class UsedbooktradeCommentListByPostId(generics.ListAPIView):
    serializer_class = UsedbooktradeCommentSerializer

    def get_queryset(self):
        Usedbookpost_id = self.kwargs['Usedbookpost_id']
        return Usedbooktrade_Comment.objects.filter(Usedbookpost_id=Usedbookpost_id)

class UsedbooktradeCommentListByParent(generics.ListAPIView):
    serializer_class = UsedbooktradeCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Usedbooktrade_Comment.objects.filter(parent_comment=parent_comment)

class UsedbooktradeCommentDetail(generics.RetrieveAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

class UsedbooktradeCommentCreate(generics.CreateAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer = UsedbooktradeCommentSerializer(data=request.data)

        if serializer.is_valid():
            # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
            # user = request.user

            user_id = serializer.validated_data["user_id"].id
            Usedbookpost_id = serializer.validated_data["Usedbookpost_id"].id
            contents = serializer.validated_data["contents"]
            
            try:
                usedbook_post = Usedbooktrade.objects.get(pk=Usedbookpost_id)
            except Usedbooktrade.DoesNotExist:
                return Response({"error": "Usedbooktrade post not found."}, status=status.HTTP_404_NOT_FOUND)

            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # serializer.save()  # 댓글을 저장하고
        
            comment = Usedbooktrade_Comment(user_id=user, Usedbookpost_id=usedbook_post, contents=contents)
            comment.save()

            usedbook_post.comment += 1
            usedbook_post.save(update_fields=['comment'])
            return Response({"message": "Comment created successfully.", "comments": usedbook_post.comment}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsedbooktradeCommentUpdate(generics.UpdateAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

class UsedbooktradeCommentDelete(generics.DestroyAPIView):
    queryset = Usedbooktrade_Comment.objects.all()

    def destroy(self, request, *args, **kwargs):

        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user

        # user_id = request.data.get("user_id")
        # Usedbookpost_id = request.data.get("Usedbookpost_id")
        comment_id = kwargs.get("pk")  # pk는 URL에서 가져온 댓글의 기본 키 값
        
        try:
            Usedbooktrade_comment = Usedbooktrade_Comment.objects.get(pk=comment_id)
        except Usedbooktrade_Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        '''
        # 댓글을 작성한 사용자와 요청한 사용자가 일치하는지 확인
        if user_id != study_comment.user_id.id:
            return Response({"error": "Unauthorized. You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        # 댓글이 속한 스터디 게시물과 요청한 스터디 게시물이 일치하는지 확인
        if studypost_id != study_comment.studypost_id.id:
            return Response({"error": "Invalid request. The comment does not belong to the specified post."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        '''

        Usedbooktrade.delete()

        # 중고거래 게시물의 댓글 수 업데이트
        try:
            usedbook_post = Usedbooktrade.objects.get(pk=Usedbooktrade_comment.Usedbookpost_id.id)
        except Usedbooktrade.DoesNotExist:
            return Response({"error": "Usedbooktrade post not found."}, status=status.HTTP_404_NOT_FOUND)

        usedbook_post.comment -= 1
        usedbook_post.save(update_fields=['comment'])

        return Response({"message": "Comment deleted successfully.", "comments": usedbook_post.comment}, status=status.HTTP_204_NO_CONTENT)



# Create your views here.
def index(request):
    return render(request,'main/index.html')

def user_view(request):
    users = User.objects.all() # user 테이블의 모든 객체 불러와서 users 변수에 저장 
    return render(request,'main/user_view.html',{'users':users})

