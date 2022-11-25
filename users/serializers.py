from rest_framework import serializers
from .models import SNUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNUser
        fields = ('id','email','last_login','last_activity')