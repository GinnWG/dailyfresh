# -*- coding:utf-8 -*-
import django
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader, RequestContext
from celery import Celery

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')

@app.task
def send_register_active_email(to_email, username, token):
    """Send active email"""
    subject = 'Dailyfresh'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, Dailyfresh' \
                       '</h1>Please click the link below to active your count<br/>' \
                       '<a href="http://127.0.0.1:8000/user/active/%s">' \
                       'http://127.0.0.1:8000/user/active/%s' \
                       '</a>' % (username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
