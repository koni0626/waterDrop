#coding:UTF-8

from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from .models import TimeCardTable


class TimeCardForm(forms.Form):
    '''初期値の設定はViewで行う'''
    username = forms.CharField(widget=forms.HiddenInput)
    date = forms.DateField(widget=forms.HiddenInput)
    #AdminTimeWidgetはイマイチ使えないので自作する
    inTime = forms.TimeField()
    offTime = forms.TimeField(required=False)
