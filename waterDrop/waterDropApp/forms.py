#coding:UTF-8

from django import forms
from django.contrib.admin import widgets

'''タイムカード入力フォーム'''
class TimeCardForm(forms.Form):
    '''初期値の設定はViewで行う'''
    username = forms.CharField(widget=forms.HiddenInput)
    date = forms.DateField(widget=forms.HiddenInput)
    inTime = forms.TimeField(widget=widgets.AdminTimeWidget)
    offTime = forms.TimeField(widget=widgets.AdminTimeWidget)
