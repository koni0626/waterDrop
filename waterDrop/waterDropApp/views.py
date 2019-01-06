from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import TimeCardTable, WorkClassTable, User
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import datetime
from dateutil.relativedelta import relativedelta
from . import utils
from . import time_card_controller

'''
ログインに関してはここが役に立つ
https://it-engineer-lab.com/archives/544
'''
# Create your views here.
@login_required
def main(request):
    '''ログイン画面表示'''

    return render(request, 'waterDropApp/index.html')

'''
ログイン画面表示
'''
def login(request):
    print("hello login")
    return render(request, 'waterDropApp/login.html',{})


@login_required
def time_card(request, code):
    """
    タイムカード表示
    :param request:
    :param code:
    :return:
    """
    if code == 'disp':
        return time_card_controller.display_time_card(request)
    elif code == 'entry':
        return time_card_controller.entry_time_card(request)


@login_required
def work_content(request, date):
    """
    作業内容表示
    :param request:
    :param date: 作業内容を表示する日時
    :return:
    """
    try:
        form = forms.WorkContentsForm()
        '''日付とユーザIDからタイムカードの主キーを取得する'''
        employee = User.objects.get(id=request.user.id)
        time_card_record = TimeCardTable.objects.get(date=date, employee=employee)
        form = forms.WorkContentsForm()

    except TimeCardTable.DoesNotExist as e:
        pass

    return render(request, 'waterDropApp/work_content.html',
                  {'time_card_record': time_card_record,
                   'form': form})


def mail(request):
    """
    メール送信テスト
    :param request:
    :return:
    """
    subject = "題名"
    message = "本文\\nです"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [
        "konickcioc@gmail.com"
    ]
    print(from_email)
    send_mail(subject, message, from_email, recipient_list)
    return render(request, 'waterDropApp/mail.html')


def create_complete(request):
    """
    ユーザが本登録されたとき
    :param request:
    :return:
    """
    return render(request, 'waterDropApp/login.html')