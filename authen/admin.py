# -*- coding:utf-8 -*-
from django.contrib import admin


from .models import ForumUser


class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('get_name',)
    # http://stackoverflow.com/questions/163823/can-list-display-in-a-django-modeladmin-display-attributes-of-foreignkey-field

    search_fields = ('get_name',)

    def get_name(self,obj):
        return obj.user.username
    get_name.admin_order_field='user'

admin.site.register(ForumUser, ForumUserAdmin)
