# -*- coding:utf-8 -*-


from django.contrib import admin
from .models import Node,Topic,Reply,Notification,Collect

# Register your models here.


class NodeAdmin(admin.ModelAdmin):
    list_display = ('name','slug','created')
    search_fields = ('name',)
    list_filter = ('created',)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','content','created_at')
    search_fields = ('title','content')
    list_filter = ('created_at',)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('content','topic')
    search_fields = ('content','topic')
    list_filter = ('updated_at',)

# 完成在 admin 界面上的工作
admin.site.register(Node,NodeAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Reply,ReplyAdmin)
admin.site.register(Collect)
admin.site.register(Notification)
