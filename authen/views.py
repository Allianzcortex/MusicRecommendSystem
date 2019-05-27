# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse

from .models import ForumUser
from .forms import registrationForm,loginForm,settingpasswordForm
from django.contrib import messages



def user_register(request):
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    '''
    user=None
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            information = form.cleaned_data
            new_user = User.objects.create_user(
                    username=information.get('username'),
                    password=information.get('password'),
                    email=information.get('email')
            )
            new_user.save()
            forumUser = ForumUser(user=new_user)
            forumUser.save()
            user=new_user
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form=registrationForm()

    context={'form':form,
             'user':user
             }
    return render(request,'authen/user_register.html',context)


def user_login(request):

    if request.method=='POST':
        form=loginForm(request.POST)
        if form.is_valid():
            information=form.cleaned_data
            user=authenticate(username=information.get('username'),
                              password=information.get('password'))
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('homepage'))
    else:
        form=loginForm()
        user=None

    context={'form':form,
             'target':{1,2,3},
             }
    return render(request,'authen/user_login.html',context)

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def user_forget_password(request):
    pass

@login_required()
def user_set_password(request):

    user = request.user if request.user else None
    if request.method=='POST':
        form=settingpasswordForm(request.POST,user=request.user)
        if form.is_valid():

            password=form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request,u'password updated successfully')
            return HttpResponseRedirect(reverse('homepage',kwargs='user'))
    else:
        form=settingpasswordForm()
    context={
        'form':form,
        'user':user,
    }


    return render(request,'authen/user_setpassword.html',context)

