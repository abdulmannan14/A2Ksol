from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    url_link = models.URLField()
    published_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
