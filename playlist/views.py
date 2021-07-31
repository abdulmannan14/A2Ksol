import datetime

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from video.models import Video
from .models import Playlist,Add_video_to_playlist
from .serializers import Playlist_serializer,Add_video_to_playlist_serializer,add_playlist_serializer,delete_playlist_serializer,\
    modify_playlist_serializer,delete_video_serializer,insert_video_serializer

from django.contrib.auth.models import User


class My_playlist(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user_id=request.user.id
        try:
            playlist=Playlist.objects.filter(assign_to__id=user_id)
            count=Playlist.objects.filter(assign_to__id=user_id).count()
            serializer=Playlist_serializer(playlist,many=True).data
            return Response({'message': 'My Playlist',
                             'status': status.HTTP_200_OK,
                             'count':count,
                             'data': serializer},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': "NOT VALID"},
                            status=status.HTTP_200_OK)

    def post(self,request):
        requested_data = request.data
        serializer = add_playlist_serializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        user_id=request.user
        name=request.data.get('name')
        try:
            if Playlist.objects.filter(name=name):
                return Response({'error': "Playlist with this name is already exists "},
                            status=status.HTTP_400_BAD_REQUEST)
            playlist=Playlist(name=name,assign_to=user_id,created_date=datetime.datetime.now())
            playlist.save()
            serializer=Playlist_serializer(playlist,many=False).data
            return Response({'message': 'Playlist Created',
                             'status': status.HTTP_200_OK,
                             'data': serializer},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': "NOT VALID"},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        requested_data = request.data
        serializer = modify_playlist_serializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        user_id=request.user.id
        playlist_id = request.data.get('playlist_id')
        name=request.data.get('name')
        try:
            if Playlist.objects.get(id=playlist_id,assign_to=user_id):
                Playlist.objects.filter(id=playlist_id,assign_to=user_id).update(name=name)
                return Response({'message': 'Playlist Updated',
                                 'status': status.HTTP_200_OK},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'You cannot modify a playlist that is not belongs to you',
                             'status': status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        requested_data = request.data
        serializer = delete_playlist_serializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        user_id=request.user.id
        playlist_id = request.data.get('playlist_id')
        try:
            if Playlist.objects.get(id=playlist_id,assign_to=user_id):
                Playlist.objects.get(id=playlist_id).delete()
                return Response({'message': 'Playlist Deleted',
                                 'status': status.HTTP_200_OK},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'You cannot delete a playlist that is not belongs to you',
                             'status': status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

class All_playlist(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user_id=request.user.id
        try:
            playlist=Playlist.objects.all()
            count=Playlist.objects.all().count()
            serializer=Playlist_serializer(playlist,many=True).data
            return Response({'message': 'All Playlists',
                             'status': status.HTTP_200_OK,
                             'count':count,
                             'data': serializer},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': "NOT VALID"},
                            status=status.HTTP_200_OK)

class My_videos(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):

        if request.data.get('playlist_id')==None:
            user_id = request.user.id
            try:
                videos = Add_video_to_playlist.objects.filter(playlist__assign_to__id=user_id)
                count = Add_video_to_playlist.objects.filter(playlist__assign_to__id=user_id).count()
                serializer = Add_video_to_playlist_serializer(videos, many=True).data
                return Response({'message': 'My Videos',
                                 'status': status.HTTP_200_OK,
                                 'count': count,
                                 'data': serializer},
                                status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return Response({'error': "NOT VALID"},
                                status=status.HTTP_200_OK)
        else:
            playlist_id = request.data.get('playlist_id')
            user_id = request.user.id
            get_playlists= Playlist.objects.filter(assign_to__id=user_id,id=playlist_id)
            if get_playlists:
                videos = Add_video_to_playlist.objects.filter(playlist__id=playlist_id)
                count=len(videos)
                serializer = Add_video_to_playlist_serializer(videos, many=True).data
                return Response({'message': 'My Videos',
                                 'status': status.HTTP_200_OK,
                                 'count': count,
                                 'data': serializer},
                                status=status.HTTP_200_OK)
            else:
                ids=[]
                get_playlists = Playlist.objects.filter(assign_to__id=user_id)
                for i in get_playlists:
                   ids.append(i.id)
                return Response({'error': "you are not authorized for this playlist",'your playlists ids are': ids},status=status.HTTP_400_BAD_REQUEST)

class Delete_video_from_my_playlist(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self,request):
        requested_data = request.data
        serializer = delete_video_serializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        user_id=request.user.id
        playlist_id=request.data.get('playlist_id')
        video_id = request.data.get('video_id')
        delete_video= Add_video_to_playlist.objects.filter(playlist__id=playlist_id,video__id=video_id)
        if delete_video:
            delete_video.delete()
            return Response({'message': 'Video Deleted',
                         'status': status.HTTP_200_OK},
                        status=status.HTTP_200_OK)
        else:
            videos_list=[]
            videos = Add_video_to_playlist.objects.filter(playlist__assign_to__id=user_id)
            for i in videos:
                videos_list.append(i.id)
            playlidt_list = []
            get_playlists = Playlist.objects.filter(assign_to__id=user_id)
            for i in get_playlists:
                playlidt_list.append(i.id)
            return Response({'message': 'Video Not Found',
                             'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                             'your videos ids are':videos_list ,
                             'your playlists ids are':playlidt_list },
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class insert_video_to_playlist(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        requested_data = request.data
        serializer = insert_video_serializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        user_id = request.user.id
        playlist_id = request.data.get('playlist_id')
        video_id = request.data.get('video_id')
        videos = Add_video_to_playlist.objects.filter(playlist__id=playlist_id,video__id=video_id)
        if videos:
            available_videos=[]
            playlist_videos_id=[]
            all_videos = Video.objects.all()
            for i in all_videos:
                available_videos.append(i.id)
            playlist_videos = Add_video_to_playlist.objects.filter(playlist__id=playlist_id)
            for i in playlist_videos:
                playlist_videos_id.append(i.video_id)
            set1 = set(available_videos)
            set2 = set(playlist_videos_id)
            remaining_videos = list(sorted(set1 - set2))
            return Response({'error':'video already present in playlist',
                             'status':status.HTTP_400_BAD_REQUEST,
                             "you can add these videos only":remaining_videos},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            videos = Add_video_to_playlist(playlist_id=playlist_id, video_id=video_id)
            videos.save()
            return Response({'message':'Video Added successfully','status':status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)
