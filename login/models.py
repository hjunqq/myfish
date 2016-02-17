from __future__ import unicode_literals

from django.db import models
# Use Django User
from django.contrib.auth.models import User
# Create your models here.

import os

class UserLogInfo(models.Model):
    user = models.ForeignKey(User)
    logInIP = models.CharField(max_length=150)
    logInTime = models.DateTimeField()
    logOutTime = models.DateTimeField()
    UserAgent = models.CharField(max_length=150)
    
    def __unicode__(self):
        return str(self.user.username)
    
    class Meta:
        db_table = 'UserLogInfo'
        verbose_name_plural='UserLogInfoes'



    
    
