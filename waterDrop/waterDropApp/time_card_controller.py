from django.shortcuts import render

from . import models
from . import forms
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta
from . import utils


def display(request):
    in_time = ""    # 出社時間
    off_time = ""   # 退社時間
    # 現在時刻取得
    now_date = timezone.localtime()
    year = now_date.year
    month = now_date.month
    day = now_date.day

    # 1か月分のレコードを作成する
    begin = datetime.datetime(year, month, 1)
    time_card_list = []

    for d in range(1, 32, 1):
        calc_date = begin + relativedelta(day=d)
        calc_month = calc_date.month
        calc_week = calc_date.weekday()
        if calc_month != month:
            # 月が替わるとループを抜ける
            break

        try:
            # 表示用フォーム作成
            record = {'date': '', 'inTime': '', 'offTime': '', 'week': '', 'kindHoliday': 0}
            employee = models.User.objects.get(id=request.user.id)
            # 社員情報の今月のデータを取得する
            record = models.TimeCardTable.objects.get(employee=employee,
                                               date__year=calc_date.year,
                                               date__month=calc_date.month,
                                               date__day=calc_date.day)
            # 社員に適用されているカレンダー基本設定を取得

            # 社員に適用されているカレンダーの詳細設定を取得
            form = forms.TimeCardForm(initial={'in_time': record.in_time,
                                               'off_time': record.off_time,
                                               'date': utils.get_hyphen_date(calc_date),
                                               'work_class': record.work_class.id})
        except models.TimeCardTable.DoesNotExist:
            form = forms.TimeCardForm(initial={'in_time': '',
                                               'off_time': '',
                                               'date': utils.get_hyphen_date(calc_date)})

        time_card_list.append({'disp_date': utils.get_slash_date(calc_date),
                               'hidden_date': utils.get_hyphen_date(calc_date),
                               'disp_week': utils.convert_week(calc_week),
                               'hidden_week': calc_week,
                               'form': form})

    return {'records': time_card_list,
                   'year': year,
                   'month': month}


def update(request):
    """
    出退勤時間を登録する
    """
    offTime = ""
    inTime = ""
    status = "success"

    if request.method == "POST":
        '''出社時間、退社時間を登録'''
        form = forms.TimeCardForm(request.POST)
        if form.is_valid():
            '''ユーザテーブルからユーザIDを取得する'''
            employee = models.User.objects.get(id=request.user.id)
            print("=================================")
            try:
                '''日付とユーザIDからタイムカードの主キーを取得する'''
                pk = models.TimeCardTable.objects.get(date=form.cleaned_data['date'], employee=employee)
                work_class = models.WorkClassTable.objects.get(name=form.cleaned_data['work_class'])
                print(work_class)
                models.TimeCardTable(id=pk.id,
                                     employee=employee,
                                     date=form.cleaned_data['date'],
                                     in_time=form.cleaned_data['in_time'],
                                     off_time=form.cleaned_data['off_time'],
                                     work_class=work_class).save()
            except models.TimeCardTable.DoesNotExist as e:
                print("こっちだよ")
                print(form.cleaned_data['work_class'])
                work_class = models.WorkClassTable.objects.get(name=form.cleaned_data['work_class'])
                print(form.cleaned_data['work_class'])
                models.TimeCardTable(
                                     employee=employee,
                                     date=form.cleaned_data['date'],
                                     in_time=form.cleaned_data['in_time'],
                                     off_time=form.cleaned_data['off_time'],
                                     work_class=work_class).save()

#        else:
#            '''データの形式が不正'''
#            print("entry error")
 #           print(form.errors)
#            status = "error"

    # return render(request, 'waterDropApp/timecard_entry.html', {"status" : status})