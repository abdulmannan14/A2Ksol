from rest_framework import serializers
from .models import Playlist,Add_video_to_playlist
from video.serializers import Video_serializer
class Playlist_serializer(serializers.ModelSerializer):
    class Meta:
        model=Playlist
        fields="__all__"



class Add_video_to_playlist_serializer(serializers.ModelSerializer):
    playlist=Playlist_serializer(Add_video_to_playlist.playlist)
    video=Video_serializer(Add_video_to_playlist.video)
    class Meta:
        model=Add_video_to_playlist
        # fields="__all__"
        fields=(
            'playlist',
            'video',
        )


class add_playlist_serializer(serializers.Serializer):
    name=serializers.CharField(max_length=50)

class delete_playlist_serializer(serializers.Serializer):
    playlist_id=serializers.IntegerField()


class modify_playlist_serializer(serializers.Serializer):
    playlist_id = serializers.IntegerField()
    name= serializers.CharField(max_length=50)

class delete_video_serializer(serializers.Serializer):
    playlist_id = serializers.IntegerField()
    video_id=serializers.IntegerField()

class insert_video_serializer(serializers.Serializer):
    playlist_id = serializers.IntegerField()
    video_id = serializers.IntegerField()