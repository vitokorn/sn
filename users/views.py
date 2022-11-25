from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import SNUser
from users.serializers import UsersSerializer




class UsersAPIList(generics.ListAPIView):
    queryset = SNUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, ]


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = SNUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, ]