from django.shortcuts import render
from django.http import HttpResponse
from .models import TimeCardTable
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone

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

'''
出勤画面表示
'''
@login_required
def timeCard(request):
    offTime = ""
    inTime = ""
    if request.method == "POST":
        '''出社時間、退社時間を登録'''
        form = forms.TimeCardForm(request.POST)
        if form.is_valid():
            '正しい'
            print(form.cleaned_data['date'])
            print(form.cleaned_data['username'])
            print(form.cleaned_data['inTime'])
            print(form.cleaned_data['offTime'])
        else:
            '間違い'
            pass
    else:
        '''表示オンリー'''
        try:
            '''現在日時を取得する'''
            nowDate = timezone.localtime().strftime("%Y-%m-%d")
            '''ここをユーザー名指定にしないとやばい'''
            record = TimeCardTable.objects.get(day=nowDate)
            inTime = record.getInTime()[0:5]
            offTime = record.getOffTime()[0:5]
            if inTime != "None":
                offTime = timezone.localtime().strftime("%H:%M")
        except TimeCardTable.DoesNotExist:
            '''まだ未入力なので現在時刻を出社時刻に設定する'''
            inTime = timezone.localtime().strftime("%H:%M")

        form = forms.TimeCardForm(initial={'inTime': inTime, 'offTime': offTime,
                                           'username': request.user.username,
                                           'date': nowDate})

    return render(request, 'waterDropApp/timecard.html', {"form": form})
