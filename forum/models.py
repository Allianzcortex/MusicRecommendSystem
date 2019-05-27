# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# from ..authen import ForumUser 

# Create your models here.


class NodeManager(models.Manager):
    '''
    Manage all the nodes
    '''

    # 返回热门节点，按照有主题的数量来排序
    def get_all_hot_Node(self):
        query = self.get_queryset().filter(topic_count__gte=0). \
            order_by('-topic_count')
        return query
        #


class Node(models.Model):
    '''
    Nodes
    '''
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    introduction = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    topic_count = models.IntegerField(default=0)

    objects = NodeManager()  # 为了进行个性化的定制


class TopicManager(models.Manager):
    '''
    Manage all the topics
    '''

    def get_all_topic(self):
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by'). \
            all().order_by('-last_replied_time', '-reply_count', '-created_at')

        return query

    def get_hot_topic(self):
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by'). \
            order_by('-reply_count')
        return query

    def get_all_topic_by_node_slug(self, node_slug):
        query = self.get_queryset().filter(node__slug=node_slug). \
            select_related('node', 'author', 'last_replied_by'). \
            order_by('-last_replied_time', '-reply_count', '-created_at')
        return query

    def get_all_topic_create_by_user(self, username=None):
        # foreignkey+onetoonefield
        query = self.get_queryset().filter(author__user__username = username). \
                select_related('node', 'author').order_by('-created_at')  # 按照创建时间排序
        return query


class Topic(models.Model):
    '''
    Topic
    '''
    title = models.CharField(max_length=128, unique=True)
    content = models.TextField()
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    reply_count = models.IntegerField(default=0)

    last_replied_time = models.DateTimeField(null=True, blank=True)
    node = models.ForeignKey(Node, related_name='node')
    author = models.ForeignKey('authen.ForumUser', related_name='topic_author')
    last_replied_by = models.ForeignKey('authen.ForumUser', related_name='last_reply_author',
                                        null=True, blank=True)

    objects = TopicManager()

    def __unicode__(self):
        return self.title


class ReplyManager(models.Manager):
    '''
    Reply
    '''

    def get_all_replies_by_topic(self, topic_id):
        query = self.get_queryset().select_related('topic', 'author'). \
            filter(topic__id=topic_id).order_by('updated_at')
        return query

    def get_hot_reply(self):
        query = self.get_queryset().select_related('topic', 'author'). \
                    filter(upvote_count__gte=0)[:10]
        return query

    def get_all_replies_by_user_id(self, user_name):
        query = self.get_queryset().select_related('topic', 'author'). \
            filter(author__user__username=user_name).order_by('-updated_at')
        return query

class Reply(models.Model):
    content = models.TextField()
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    agree_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    topic = models.ForeignKey(Topic, related_name='reply')
    author = models.ForeignKey('authen.ForumUser', related_name='reply_author')

    objects = ReplyManager()

    def __unicode__(self):
        return self.content


class CollectManager(models.Manager):

    def get_all_collection_by_user(self, user_id):
        query = self.get_queryset().select_related('collect_user', 'collect_topic', ). \
            filter(collect_user__id=user_id).order_by('collected_at')
        return query


class Collect(models.Model):

    collect_user = models.ForeignKey('authen.ForumUser', on_delete=models.CASCADE,
                                     related_name='user_collect')
    collect_topic = models.ForeignKey(Topic, related_name='topic_collect')
    collected_at = models.DateTimeField(auto_now=True)

    objects = CollectManager()


class NotificationManager(models.Manager):

    def get_all_notifications_for_user(self, user_id):
        query = self.get_queryset().select_related('involved_topic', 'involved_user', 'trigger_user'). \
            filter(trigger_user__id=user_id).order_by('-occurence_time')
        return query


class Notification(models.Model):
    
    status = models.IntegerField(default=0)  # 0 is unread, 1 is read
    content = models.TextField()
    involved_type = models.IntegerField(default=0)  # 0 is no-reply, 1 is reply
    involved_user = models.ForeignKey('authen.ForumUser', related_name='notify_user')
    involved_topic = models.ForeignKey(Topic, related_name='notify_topic')
    involved_reply = models.ForeignKey(Reply, related_name='notify_reply')
    trigger_user = models.ForeignKey('authen.ForumUser', related_name='trigger_user')
    occurence_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content
