from django.shortcuts import render, redirect
import re
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from itsdangerous import TimedSerializer
from itsdangerous import SignatureExpired

User = get_user_model()


# def register(request):
#     # load register page
#     if request.method == 'GET':
#         return render(request, 'register.html')
#     # get personnel data from register.html
#     else:
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         password2 = request.POST.get('cpwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#
#         # verify
#         # data incomplete
#         if not all([username, password, email]):
#             return render(request, 'register.html', {'errmsg': 'data incomplete'})
#         # email
#         if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': 'email form illegal'})
#
#         # psw
#         if not password == password2:
#             return render(request, 'register.html', {'errmsg': 'password non correspondent'})
#
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': 'non accept contract'})
#
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # user non exist
#             user = None
#         # user exist
#         if user:
#             print('===user exist===')
#             return render(request, 'register.html', {'errmsg': 'user exist'})
#
#         print('------------')
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0
#         user.save()
#         return redirect(reverse('index'))

# def login(request):
#     return render(request, 'login.html')


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

        # psw
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

        print('------------')
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # activity login
        # mask user ID by itsdangerous
        # Time out 3600s = 1 hour
        serializer = TimedSerializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dump(info)

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
        return render(request, 'login.html')
