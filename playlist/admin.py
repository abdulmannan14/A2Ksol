from django.contrib import admin
from .models import Playlist,Add_video_to_playlist




class All_playlist(admin.ModelAdmin):
    list_display = ('name','assign_to','created_date')
admin.site.register(Playlist,All_playlist)


class Playlist_details(admin.ModelAdmin):
    list_display = ('playlist_name','playlist_assign_to','playlist_created_date')

    def playlist_name(self, Add_video_to_playlist):
        return Add_video_to_playlist.playlist.name


    def playlist_assign_to(self, Add_video_to_playlist):
        return Add_video_to_playlist.playlist.assign_to

    def playlist_created_date(self, Add_video_to_playlist):
        return Add_video_to_playlist.playlist.created_date


admin.site.register(Add_video_to_playlist,Playlist_details)