from django.contrib import admin
from django.urls import path,include
from accounts.views import LoginAPI,Register
from video.views import Get_videos
from playlist.views import My_playlist,My_videos,All_playlist,Delete_video_from_my_playlist,insert_video_to_playlist





accounts_patterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
]
video_patterns = [
    path('', Get_videos.as_view(), name='playlist'),
]

playlist_patterns=[
    path('all_playlists/', All_playlist.as_view(), name='playlist'),
    path('my_playlist/', My_playlist.as_view(), name='playlist'),
    path('my_videos/', My_videos.as_view(), name='videos'),
    path('my_video_add/', insert_video_to_playlist.as_view(), name='add_video'),
    path('my_video_delete/', Delete_video_from_my_playlist.as_view(), name='remove_video'),

]

api_patterns = [
    path('', include(accounts_patterns)),
    path('videos/', include(video_patterns)),
    path('playlists/', include(playlist_patterns)),

]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]


