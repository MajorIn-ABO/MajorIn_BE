from rest_framework import serializers
from .models import User, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like, Usedbooktrade, UsedbooktradeData, Usedbooktrade_Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'user_id', 'category_id', 'title', 'contents']

class BoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_Comment
        fields = ['id', 'user_id', 'post_id', 'contents']

class BoardLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_Like
        fields = ['id', 'user_id', 'post_id']

class BoardBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_bookmark
        fields = ['id', 'user_id', 'post_id']

class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ['id', 'user_id', 'title', 'contents', 'hashtags', 'is_recruited']

class StudyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Comment
        fields = ['id', 'user_id', 'studypost_id', 'contents']   

class StudyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Like
        fields = ['id', 'user_id', 'studypost_id'] 

class UsedbooktradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usedbooktrade
        fields = ['id', 'title', 'author', 'seller', 'publisher', 'price', 'imgfile', 'description', 'damage_level', 'post_date', 'is_sold']

class UsedbooktradeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedbooktradeData
        fields = ['id', 'trade', 'sellerid', 'sell_date']

class UsedbooktradeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usedbooktrade_Comment
        fields = ['id', 'user_id', 'Usedbookpost_id', 'contents']    