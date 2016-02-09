from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django_comments.models import Comment

# Create your models here.

def get_image_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)
       
class DailyContent(models.Model):
    user = models.ForeignKey(User,related_name="post_by")
    date = models.DateField()
    sentence = models.CharField(blank=True,max_length=500)
    author = models.CharField(blank=True,max_length=100)
    img = models.ImageField(upload_to=get_image_path)
    likedby = models.ManyToManyField(User,related_name="liked_by",blank=True)
    comments = models.ManyToManyField(Comment,related_name="comment_by",blank=True)
    def __unicode__(self):
        return str(self.date)
    
    class Meta:
        db_table = 'DailyContent'
