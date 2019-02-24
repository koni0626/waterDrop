# coding:UTF-8
from . import models
from . import forms
from django.shortcuts import render

def display(request, date):
    work_table_forms = []
    try:
        '''日付とユーザIDからタイムカードの主キーを取得する'''
        employee = models.User.objects.get(id=request.user.id)
        time_card = models.TimeCardTable.objects.get(date=date, employee=employee)
        work_table_records = models.WorkTable.objects.filter(time_card=time_card)
        for record in work_table_records:
            work_table_forms.append(forms.WorkContentsForm(initial={
                "work_code": record.work_code,
                "work_time": record.work_time
            }))
        work_table_forms.append(forms.WorkContentsForm())

    except models.TimeCardTable.DoesNotExist as e:
        work_table_forms.append(forms.WorkContentsForm())

    return render(request, 'waterDropApp/work_content.html',
                  {'work_table_forms': work_table_forms,
                   'date': date})


def update(request, date):
    employee = models.User.objects.get(id=request.user.id)
    if request.method == "POST":
        '''出社時間、退社時間を登録'''
        form = forms.WorkContentsForm(request.POST)
        if form.is_valid():
            print("工事中")