from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from . import time_card_controller
from . import work_content_controller
from . import models
from django.http import HttpResponse, HttpResponseRedirect
'''
ログインに関してはここが役に立つ
https://it-engineer-lab.com/archives/544
'''
# Create your views here.
@login_required
def main(request):
    '''ログイン画面表示'''

    return render(request, 'waterDropApp/index.html')


def login(request):
    """
    ログイン画面表示
    :param request:
    :return:
    """
    return render(request, 'waterDropApp/login.html',{})


@login_required
def time_card(request, code):
    """
    タイムカード表示
    :param request:
    :param code:
    :return:
    """
    # パラメーター読み込み
    location_op = models.OptionTable.objects.get(name="get_location")

    if code == 'disp':
        response = time_card_controller.display(request)
        response["location_op"] = location_op.value
        return render(request,
                      'waterDropApp/time_card.html',
                      response)

    elif code == 'update':
        print(request.POST["lat"])
        time_card_controller.update(request)
        return HttpResponseRedirect("/time_card/disp")


@login_required
def work_content(request, code, date):
    """
    作業内容表示
    :param request:
    :param date: 作業内容を表示する日時
    :return:
    """
    # コントローラーは継承で作ったほうがよいか？
    if code == 'disp':
        return work_content_controller.display(request, date)
    elif code == 'update':
        return work_content_controller.update(request, date)


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