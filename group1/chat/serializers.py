from .models import Room
from rest_framework import routers, serializers, viewsets, filters


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('title', 'staff_only')
