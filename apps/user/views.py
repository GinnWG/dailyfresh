from django.shortcuts import render, redirect
import re
from django.contrib.auth.models import User
import apps.goods.views as goods_view

# Create your views here.

# /user/register
from django.urls import reverse


def register(request):
    return render(request, 'register.html')


def register_handle(request):
    # get personnel data from register.html
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    password2 = request.POST.get('cpwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    # verify
    # data incomplete
    if not all([username, password, email]):
        return render(request, 'register.html', {'errmsg': 'data incomplete'})
    # email
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': 'email form illegal'})

    # psw
    # if not password == password2:
    #     return render(request, 'register.html', {'errmsg': 'password non correspondent'})

    if allow != 'on':
        return render(request, 'register.html', {'errmsg': 'non accept contract'})

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # user non exist
        user = None
    # user exist
    if user:
        return render(request, 'register.html', {'errmsg': 'user exist'})

    user = User.objects.create_user(username, email, password)
    user.is_active = 0
    user.save()
    return redirect(reverse('goods'))


def login(request):
    return render(request, 'login.html')
