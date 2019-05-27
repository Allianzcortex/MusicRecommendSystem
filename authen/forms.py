# -*- coding:utf-8 -*-

from .models import ForumUser
from django import forms
from django.conf import settings 
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

error_messages = {
    'username': {
        'required': u'username can not be empty',
        'min_length': u'username is too short, it should be between 5-128 characters',
        'max_length': u'username is too long, it should be between 5-128 characters',
        'invalid': u'username is in wrong format, only numbers/letters/underscore allowed',
    },
    'email': {
        'required': u'email address can not be emtpy',
        'invalid': u'email address is in wrong format',
    },
    'password': {
        'required': u'password can not be empty',
        'min_length': u'password is too short, it should be between 4-15 characters',
        'max_length': u'password is too long, it should be between 4-15 characters',
    }
}


class registrationForm(forms.Form):
    username = forms.CharField(help_text='Please type your username', min_length=5, max_length=128)
    password = forms.CharField(help_text='Please type your password', min_length=5, max_length=128)
    password_repeat = forms.CharField(help_text='Please repeat your password', min_length=5, max_length=128)
    email = forms.EmailField(help_text='Please type your email address')

    # TODO the following fields can be implemented later
    # github = forms.URLField()
    # website = forms.URLField()
    

    class Meta:
        model = ForumUser
        exclude = ['user', 'fortune', 'updated', ]

    def clean_username(self):
        
        username = self.cleaned_data.get('username')
        try:
            user = ForumUser.objects.get(user__username=username)
            raise forms.ValidationError(u'username is registered')
        except ForumUser.DoesNotExist:
            if username in settings.RESERVED:
                raise forms.ValidationError(u'username includes illegal words')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            email = ForumUser.objects.get(user__email=email)
            raise forms.ValidationError(u'email has been registered')
        except ForumUser.DoesNotExist:
            return email

    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError(u'password confirmation error')
        return password_repeat

    def save(self):
        user = super(registrationForm, self).save()
        return user


class loginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=128,
                               help_text=u'Please type user name',
                               error_messages=error_messages.get('username'))
    password = forms.CharField(min_length=5, max_length=128,
                               help_text=u'Please type user password',
                               error_messages=error_messages.get('password'))

    def __init__(self, *args, **kwargs):

        super(loginForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'
        self.helper.layout=Layout(
            'username',
            'password',

        )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(u'Username or password is incorrect')
        elif not user.is_active:
            raise forms.ValidationError(u'This user is not activated currently')

        return self.cleaned_data


class settingpasswordForm(forms.Form):

    password_old = forms.CharField(min_length=4, max_length=128,
                                   help_text=u'Please type current password')

    password_new = forms.CharField(min_length=4, max_length=128,
                                   error_messages=error_messages.get('password'),
                                   help_text='Please type new password')
    password_repeat = forms.CharField(min_length=4, max_length=128,
                                      error_messages=error_messages.get('password'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(settingpasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password_old = self.cleaned_data.get('password_old')
        password_new = self.cleaned_data.get('password_new')
        password_repeat = self.cleaned_data.get('password_repeat')

        if not self.user.check_password(password_old):
            raise forms.ValidationError(u'current password is incorrect')
        if password_new != password_repeat:
            raise forms.ValidationError(u'repeated password does not match previous one')
        return self.cleaned_data
