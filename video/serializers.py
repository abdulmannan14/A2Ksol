from rest_framework import serializers
from .models import Video


class Video_serializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"