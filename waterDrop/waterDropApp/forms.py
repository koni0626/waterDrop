#coding:UTF-8

from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from . import models

from django.contrib.admin.widgets import AdminTimeWidget


class TimeCardForm(forms.Form):
    # 初期値の設定はViewで行う
    date = forms.DateField(widget=forms.HiddenInput)
    # AdminTimeWidgetはイマイチ使えないので自作する
    in_time = forms.TimeField(widget=AdminTimeWidget, required=False)
    off_time = forms.TimeField(widget=AdminTimeWidget, required=False)
    work_class = forms.ModelChoiceField(label='勤務区分',
                                        widget=forms.Select,
                                        queryset=models.WorkClassTable.objects.all(),
                                        required=True)

class WorkContentsForm(forms.Form):
    """
    作業内容のフォーム
    """
    records = models.PersonalWorkStatusTable.objects.all()
    choice_list = [(0, "-----")]
    for record in records:
        choice_list.append((record.id, record.name))
        print((record.id, record.name))

    personal_status = forms.ChoiceField(label='休暇区分',
                                        widget=forms.Select,
                                        choices=choice_list,
                                        required=False)

    work_code = forms.ModelChoiceField(label='作番コード',
                                       queryset=models.WorkCodeTable.objects.all())

    work_detail_code = forms.ModelChoiceField(label='作業コード',
                                              queryset=models.WorkDetailCodeTable.objects.all())

    work_time = forms.TimeField(label='作業時間',
                                widget=AdminTimeWidget,
                                required=False)

    """
    https://qiita.com/maisuto/items/33dfeb58f5953d1c5fdf
    にDBからの複数選択肢をDBから取得する方法が載っている
    
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = question.choice_set.all()
    """