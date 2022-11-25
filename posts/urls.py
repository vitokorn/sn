from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostAPIList.as_view(), name='posts'),
    path('create/', views.PostAPICreate.as_view(), name='post_create'),
    path('<int:pk>',views.PostDetailAPIView.as_view(), name='post'),
    path('like/', views.PostStatisticAPILike.as_view(), name='like'),
    path('dislike/', views.PostStatisticAPIDislike.as_view(), name='dislike'),
    path('analytics/',views.AnalyticsView.as_view(),name='analytics'),
    path('analytics2/', views.AnalyticsView2.as_view(), name='analytics'),
]
