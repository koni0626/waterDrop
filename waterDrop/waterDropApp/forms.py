#coding:UTF-8

from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from .models import TimeCardTable, CalendarTable, WorkClassTable, PersonalWorkStatusTable
from django.contrib.admin.widgets import AdminTimeWidget


class TimeCardForm(forms.Form):
    # 初期値の設定はViewで行う
    date = forms.DateField(widget=forms.HiddenInput)
    # AdminTimeWidgetはイマイチ使えないので自作する
    in_time = forms.TimeField(widget=AdminTimeWidget, required=False)
    off_time = forms.TimeField(widget=AdminTimeWidget, required=False)
    records = WorkClassTable.objects.all()
    choice_list = [(0, "-----")]
    for record in records:
        choice_list.append((record.id, record.name))
        print((record.id, record.name))
    work_class = forms.ChoiceField(label='勤務区分',
                                   widget=forms.Select,
                                   choices=choice_list,
                                   required=True)


class WorkContentsForm(forms.Form):
    records = PersonalWorkStatusTable.objects.all()
    choice_list = [(0, "-----")]
    for record in records:
        choice_list.append((record.id, record.name))
        print((record.id, record.name))

    personal_status = forms.ChoiceField(label='休暇区分',
                                        widget=forms.Select,
                                        choices=choice_list,
                                        required=False)
