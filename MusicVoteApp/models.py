from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class MusicChannelSong(models.Model):
    song_url  = models.URLField(max_length = 200)
    video_id  = models.CharField(max_length = 100)

    def get_iframe(self):
        return "<iframe id='player' type='text/html' width='640' height='390' src='http://www.youtube.com/embed/{0}?enablejsapi=1' frameborder='0'></iframe>".format(self.video_id)

    def slice_video_id(self):
        return self.song_url.split("v=")[1]

    def save(self, *args, **kwargs):
        self.video_id = self.slice_video_id()
        super(MusicChannelSong, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}".format(self.video_id)

class MusicChannel(models.Model):
    channel_name  = models.CharField(max_length = 20, unique = True)
    creation_date = models.DateTimeField('date created')
    slug          = models.SlugField(unique = True)
    channel_songs = models.ManyToManyField(MusicChannelSong)

    def add_song(self, new_song):
        self.channel_songs.add(new_song)

    def get_songs(self):
        return self.channel_songs.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.channel_name)
        super(MusicChannel, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}".format(self.channel_name)

class Message(models.Model):
    message_text = models.TextField()
    posted_by    = models.ForeignKey(User)
    channel_name = models.ForeignKey(MusicChannel)
    date_posted  = models.DateTimeField('date posted')
    
    def __unicode__(self):
        return "{0} [{1}]: {2}".format(self.posted_by, self.date_posted, self.message_text)