# -*- coding:utf-8 -*-
from django import forms
from django.conf import settings

error_messages = {
    'title': {
        'required': u'title can not be empty',
        'max_length': u'title is too long',
    },
    'content': {
        'required': u'content can not be empty',
    }
}


class CreateForm(forms.Form):
    # 创建主题的内容
    title = forms.CharField(max_length=128, help_text=u'Please type your title',
                            error_messages=error_messages.get('title'))
    content = forms.CharField(widget=forms.Textarea,
                              error_messages=error_messages.get('content'))
    '''
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
    '''
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in settings.LAW_RESERVED:
            raise forms.ValidationError(u'Illegal character in post')
        return title

    def clean_content(self):
        '''
        content = self.cleaned_data.get('content')
        for str in settings.LAW_RESERVED:
            if content.find(str):
                raise forms.ValidationError(u'Illegal content')
        '''
        return self.cleaned_data.get('content')

class ReplyForm(forms.Form):
    content=forms.CharField(widget=forms.Textarea,
                            error_messages=error_messages.get('content'))
