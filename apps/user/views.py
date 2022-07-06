import smtplib

from django.shortcuts import render, redirect
import re
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse
from utils.mixin import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from itsdangerous import TimedSerializer
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_register_active_email

User = get_user_model()


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
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

        # pwd
        if not password == password2:
            return render(request, 'register.html', {'errmsg': 'password non correspondent'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': 'non accept contract'})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # user non exist
            user = None
        # user exist
        if user:
            print('===user exist===')
            return render(request, 'register.html', {'errmsg': 'user exist'})

        user = User.objects.create_user(username, email, password)
        user.is_active = 1 # During the send email no work user.is_active = 0
        user.save()

        # activity login
        # mask user ID by itsdangerous
        # Time out 3600s = 1 hour
        serializer = TimedSerializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        # token = str(b'serializer.dumps(info)', "utf-8")
        token = serializer.dumps(info)
        token = token.decode("utf-8")

        # send pre user email
        send_register_active_email.delay(email, username, token)
        return redirect(reverse('index'))

class ActiveView(View):
    def get(self, request, token):
        serializer = TimedSerializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.load(token)
            # get user id
            user_id = info['confirm']
            # get user
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # redirect to login
            return redirect(reverse('login'))
        except SignatureExpired as err:
            # Secret key is time out
            return HttpResponse('Secret key is time out')


class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            password = request.COOKIES.get('pwd')

            print(username + ": " + password)
            checked = 'checked'
        else:
            username = ''
            password = ''
            checked = ''
        return render(request, 'login.html', {'username': username, 'pwd': password, 'checked': checked})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': 'non complete'})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                # get url after login, index by default
                next_url = request.GET.get('next', reverse('index'))

                response = redirect(next_url)
                remember = request.POST.get('remember')

                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600) # one week
                    response.set_cookie('pwd', password, max_age=7*24*3600)
                else:
                    response.delete_cookie('username', 'pwd')
                # print("User is valid, active and authenticated.")
                return response
            else:
                # print("The password is valid, but the account has been disabled.")
                return render(request, 'login.html', {'errmsg': 'account has been disabled.'})
        else:
            # print("The username or password were incorrect.")
            return render(request, 'login.html', {'errmsg': 'username or password were incorrect.'})

class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        # get user info
        return render(request, 'user_center_info.html', {'page': 'user'})

class UserOrderView(LoginRequiredMixin, View):
    def get(self, request):
        # get order
        return render(request, 'user_center_order.html', {'page': 'order'})

class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_site.html', {'page': 'address'})

    def post(self, request):
        receiver = request.POST.get('receiver')

        return render(request, 'user_center_site.html', {'page': 'address'})


class LogoutView(View):
    """退出登录"""
    def get(self, request):
        logout(request)

        return redirect(reverse('goods:index'))

