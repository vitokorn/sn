from . import views
from django.urls import path
from rest_framework import routers

# router = routers.DefaultRouter(r'api')
# router.register('list',views.PostAPIList)

urlpatterns = [
    path('activity', views.UsersAPIList.as_view(), name='activity'),
    path('<int:pk>', views.UserDetailAPIView.as_view(), name='user'),
]
