from django.db import models
from video.models import Video
from django.contrib.auth.models import User

class Playlist(models.Model):
    name = models.CharField(max_length=100,unique=True)
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Add_video_to_playlist(models.Model):
    playlist=models.ForeignKey(Playlist,on_delete=models.CASCADE,blank=False)
    video=models.ForeignKey(Video,on_delete=models.CASCADE,blank=False)

    def __str__(self):
        return self.playlist.name