# -*- coding:utf-8 -*-
import json, hashlib, math

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Topic, Reply, Notification, Collect, Node
# from cortexForum.authen.models import ForumUser
from .forms import CreateForm, ReplyForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json as simplejson

def get_homepage(request):
    user = request.user

    topics = Topic.objects.get_all_topic()
    paginator=Paginator(topics,10)
    page=request.GET.get('page')
    try:
        topics=paginator.page(page)
    except PageNotAnInteger:
        topics=paginator.page(1)
    except EmptyPage:
        topics=paginator.page(paginator.num_pages)

    pagerank=[x+1 for x in xrange(topics.paginator.num_pages)]

    hot_nodes = Node.objects.get_all_hot_Node()
    hot_topics = Topic.objects.get_hot_topic()
    hot_replies = Reply.objects.get_hot_reply()


    node_count = Node.objects.all().count()
    topic_count = Topic.objects.all().count()
    reply_count = Reply.objects.all().count()
    target = {1, 2, 3}
    notifications_count=Notification.objects.filter(status=0).count()
    context = {
        'user': user,
        'topics': topics,
        'hot_nodes': hot_nodes,
        'hot_topics': hot_topics,
        'hot_replies': hot_replies,
        'node_count': 1,
        'topic_count': topic_count,
        'reply_count': reply_count,
        'target': {1, 2, 3},
        'notifications_count':notifications_count,
        'pagerank':pagerank,
    }

    return render(request, 'forum/homepage.html', context)


def get_topic(request, topic_id=None):

    user = request.user if request.user.is_authenticated() else None
    reply = Reply.objects.get_all_replies_by_topic(topic_id=topic_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = Reply(
                    content=form.cleaned_data.get('content')
            )
            topic = Topic.objects.get(id=topic_id)
            reply.topic = topic
            reply.author_id = user.id
            reply.save()
            reply_count = topic.reply_count + 1
            topic.reply_count=reply_count
            topic.save()
            if user.id != topic.author_id:
                notification=Notification(
                    content=form.cleaned_data.get('content'),
                    involved_user=topic.author,
                    involved_topic=topic,
                    involved_reply=reply,
                    trigger_user=user.forumuser,
                )
                noti=[]
                noti.append(notification)
                Notification.objects.bulk_create(noti)



            return HttpResponseRedirect(reverse('get_topic', kwargs={'topic_id': topic_id}))

    else:
        form = ReplyForm()
    topic=Topic.objects.get(id=topic_id)

    context = {
        'user': user,
        'reply': reply,
        'form': form,
        'topic':topic,
    }

    return render(request, 'forum/get_topic.html', context)

@login_required()
def create_topic(request, slug=None):

    user = request.user
    node = get_object_or_404(Node, slug=slug)

    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            topic = Topic(
                    title=form.cleaned_data.get('title'),
                    content=form.cleaned_data.get('content'),
                    node=node,
            )
           
            topic.author_id = user.id
            topic.save()
            node.topic_count = node.topic_count + 1

            return HttpResponseRedirect(reverse('homepage'))
            # httpresponseredirect vs redirect : 
            # http://stackoverflow.com/questions/13304149/what-the-difference-between-using-django-redirect-and-httpresponseredirect
    else:
        form = CreateForm()

    context = {
        'user': user,
        'form': form,
        'slug': slug,
    }
    return render(request, 'forum/create_topic.html', context)


def get_topic_by_node(request, slug):

    user = request.user
    node_topic = Topic.objects.get_all_topic_by_node_slug(node_slug=slug)
    context = {
        'user': user,
        'node_topic': node_topic,
        'slug':slug,
    }
    return render(request, 'forum/get_topic_node.html', context)


def upvote(request):
    if request.is_ajax():
        upvote_count = request.POST.get('upvote_count', '')
        id = request.POST.get('reply_id', '')
        reply = Reply.objects.get(id=reply_id)
        reply.update(
                upvote_count=upvote_count,
                agree_count=upvote_count - reply.downvote_count,
        )
        respose_dict = {
            'upvote_count': upvote_count,
        }
        return HttpResponse(simplejson.dumps(respose_dict), mimetype="application/json")
        # return render(request,'forum/upvote.html')

def get_user_profile(request,user_name):

    user=User.objects.get(username=user_name)
    user_topic=Topic.objects.get_all_topic_create_by_user(user.username)
    user_reply=Reply.objects.get_all_replies_by_user_id(user.username)

    context={
        'username':user.username,
        'introduce':user.forumuser.introduce,
        'fortune':user.forumuser.fortune,
        'updated':user.forumuser.updated,
        'website':user.forumuser.website,
        'github':user.forumuser.github,
        'douban':user.forumuser.douban,
        'weibo':user.forumuser.weibo,

        'user_topic':user_topic,
        'user_reply':user_reply,
    }
    return render(request,'authen/user_profile.html',context)

def get_wiki(request):
    return render(request,'forum/wiki.html')
