from django.contrib import admin
from .models import Video
# Register your models here.



class Video_details(admin.ModelAdmin):
    list_display = ('title','url_link','published_date')

admin.site.register(Video,Video_details)