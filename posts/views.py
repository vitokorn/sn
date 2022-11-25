from django.db.models import Count, Case, When

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from .filters import DateRangeFilterSet
from .models import Post, PostStatistic,PostAnalytics
from .serializers import PostSerializer, PostLikeSerializer, PostDislikeSerializer,PostStatisticSerializerNew
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db import connection


class PostAPIList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostAPICreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostStatisticAPILike(generics.CreateAPIView):
    queryset = PostStatistic.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        post_id = request.data['post_id']
        user_id = request.data['user_id']
        if PostStatistic.objects.filter(post_id=post_id,user_id=user_id,dislike=True).exists():
            PostStatistic.objects.filter(post_id=post_id, user_id=user_id, dislike=True).last().delete()
        self.create(request, *args, **kwargs)
        return Response(status=201,data={'message':f'Post {post_id} successfully liked'})


class PostStatisticAPIDislike(generics.CreateAPIView):
    queryset = PostStatistic.objects.all()
    serializer_class = PostDislikeSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        post_id = request.data['post_id']
        user_id = request.data['user_id']
        if PostStatistic.objects.filter(post=post_id,user=user_id,like=True).exists():
            PostStatistic.objects.filter(post=post_id, user=user_id, like=True).last().delete()
        self.create(request, *args, **kwargs)
        return Response(status=201,data={'message':f'Post {post_id} successfully disliked'})


class AnalyticsView(generics.GenericAPIView):
    queryset = PostStatistic.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DateRangeFilterSet
    serializer_class = PostStatisticSerializerNew
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        ordered_queryset = filtered_queryset.order_by('created_at_date')

        grouped_set = ordered_queryset.values('created_at_date').annotate(like_count=Count(Case(When(like=True, then=1))),dislike_count=Count(Case(When(dislike=True, then=1))))

        analytics = []
        for data in grouped_set:
            analytics.append(
                {
                    'date': data['created_at_date'],
                    'total_likes': data['like_count'],
                    'total_dislikes': data['dislike_count'],

                }
            )
        if not analytics:
            return Response(status=404)
        return Response(analytics)


class AnalyticsView2(generics.GenericAPIView):
    queryset = PostStatistic.objects.all()
    serializer_class = PostStatisticSerializerNew

    def get(self, request, format=None):
        cursor = connection.cursor()
        query = "SELECT created_at_date as date,COUNT(case when like then 1 end) as likes,COUNT(case when dislike then 1 end) as dislikes FROM posts_poststatistic "
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from and date_to:
            query += f"WHERE created_at_date >= '{date_from}' AND created_at_date <= '{date_to}' "
        elif date_from:
            query += f"WHERE created_at_date >= '{date_from}' "
        elif date_to:
            query += f"WHERE created_at_date <= '{date_to}' "
        query += "GROUP BY created_at_date ORDER BY created_at_date"
        cursor.execute(query)
        result = cursor.fetchall()
        stat = []
        for res in result:
            stat.append(PostAnalytics(date=res[0], likes=res[1], dislikes=res[2]))
        if not stat:
            return Response(status=404)
        data = PostStatisticSerializerNew(stat, many=True)
        return Response(data.data)
