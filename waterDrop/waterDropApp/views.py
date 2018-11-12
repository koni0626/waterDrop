from django.shortcuts import render
from django.http import HttpResponse
from .models import TimeCardTable, User
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import datetime
from dateutil.relativedelta import relativedelta

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
    inTime = ""    #出社時間
    offTime = ""   #退社時間

    #表示用フォーム作成
    form = forms.TimeCardForm()

    #現在時刻取得
    nowDate = timezone.localtime()
    year = nowDate.year
    month = nowDate.month
    day = nowDate.day

    #1か月分のレコードを作成する
    beginMonthDay = datetime.datetime(year, month, 1)
    timeCardList = []
    for d in range(1, 32, 1):
        calcDate = beginMonthDay + relativedelta(day=d)
        calcMonth = calcDate.month
        calcWeekDay = calcDate.weekday()
        if calcMonth != month:
            #月が替わるとループを抜ける
            break

        try:
            record = {'date':'', 'inTime':'', 'offTime':'', 'week':'', 'kindHoliday':0}
            employee_id = request.user.id
            #社員情報の今月のデータを取得する
            record = TimeCardTable.objects.filter(employee_id=employee_id, date__year=calcDate.year, date__month=calcDate.month, date__day=calcDate.day).first()
            #社員に適用されているカレンダー基本設定を取得

            #社員に適用されているカレンダーの詳細設定を取得

            if record != None:
                print(record)
                timeCardList.append({'date': "{}/{}/{}".format(calcDate.year, calcDate.month, calcDate.day),
                                     'inTime': record.getInTime(), 'offTime': record.getOffTime(), 'weekDay':calcWeekDay})
            else:
                timeCardList.append({'date': "{}/{}/{}".format(calcDate.year, calcDate.month, calcDate.day),
                                     'inTime': '', 'offTime': '', 'weekDay':calcWeekDay})

        except TimeCardTable.DoesNotExist:
            #まだ未入力なので現在時刻を出社時刻に設定する
            print("ない")

    return render(request, 'waterDropApp/newentry.html', {"records":timeCardList, "year":year, "month":month, "forms":form})

'''
出退勤時間を登録する
'''
def timeCardEntry(request):
    offTime = ""
    inTime = ""
    status = "success"
    if request.method == "POST":
        '''出社時間、退社時間を登録'''
        form = forms.TimeCardForm(request.POST)
        if form.is_valid():
            '''ユーザテーブルからユーザIDを取得する'''
            username = form.cleaned_data['username']
            employee_id = User.objects.get(username=username)
            try:
                '''日付とユーザIDからタイムカードの主キーを取得する'''
                pk = TimeCardTable.objects.get(date=form.cleaned_data['date'], employee_id=employee_id)
                print(pk.id)
                TimeCardTable(id = pk.id, employee_id = employee_id, date = form.cleaned_data['date'],
                            inTime=form.cleaned_data['inTime'], offTime = form.cleaned_data['offTime']).save()
            except TimeCardTable.DoesNotExist as e:
                '''レコードがない場合は，出社時間とみなす'''
                TimeCardTable(employee_id = employee_id, date = form.cleaned_data['date'],
                            inTime=form.cleaned_data['inTime'], offTime = form.cleaned_data['offTime']).save()
        else:
            '''データの形式が不正'''
            print("timeCartEntry error")
            status = "error"

    return render(request, 'waterDropApp/timecard_entry.html', {"status" : status})


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
    print("きた")