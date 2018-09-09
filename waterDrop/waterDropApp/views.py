from django.shortcuts import render
from django.http import HttpResponse
from .models import AttendTable
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

'''
ログインに関してはここが役に立つ
https://it-engineer-lab.com/archives/544
'''
# Create your views here.
@login_required
def main(request):
    '''ログイン画面表示'''
    records = AttendTable.objects.all()
    RtnTable = []
    for record in records:
        user_id = record.user_id_id
        user_record = User.objects.get(id=1)
        full_name = user_record.last_name + user_record.first_name
        RtnTable.append({"full_name":full_name, "startDate":record.get_startDate, "endDate":record.get_endDate})

    return render(request, 'waterDropApp/index.html', {"attendTable":RtnTable})

'''
ログイン画面表示
'''
@login_required
def login(request):
    print("hello login")
    return render(request, 'waterDropApp/login.html',{})
