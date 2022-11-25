from rest_framework import serializers
from .models import Post,PostStatistic


class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Post
        fields = ('id','title','description','author_id')


class PostLikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PostStatistic
        fields = ('post_id','like','user_id')



class PostDislikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PostStatistic
        fields = ('post_id','dislike','user_id')


class PostStatisticSerializerNew(serializers.Serializer):
    date = serializers.CharField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()

    class Meta:
        fields = ('date','total_likes','total_dislikes')
