# Generated by Django 3.2.4 on 2021-07-31 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
        ('playlist', '0003_alter_add_video_to_playlist_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_video_to_playlist',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.video'),
        ),
    ]
