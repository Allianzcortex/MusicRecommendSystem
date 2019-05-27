# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ForumUser(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='images', blank=True)
    introduce = models.CharField(max_length=128, blank=True)
    fortune = models.IntegerField(default=42)  
    updated = models.DateTimeField(default=timezone.now())
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    
    def __unicode__(self):
        return self.user.username
