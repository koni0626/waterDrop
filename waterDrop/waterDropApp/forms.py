#coding:UTF-8

from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from .models import TimeCardTable
from django.contrib.admin.widgets import AdminTimeWidget

class TimeCardForm(forms.Form):
    '''初期値の設定はViewで行う'''
    username = forms.CharField(widget=forms.HiddenInput)
    date = forms.DateField(widget=forms.HiddenInput)
    #AdminTimeWidgetはイマイチ使えないので自作する
    inTime = forms.TimeField(widget = AdminTimeWidget)
    offTime = forms.TimeField(widget = AdminTimeWidget, required=False)
