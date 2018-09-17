from django.shortcuts import render
from django.http import HttpResponse
#from .models import AttendTable
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

    return render(request, 'waterDropApp/index.html')

'''
ログイン画面表示
'''
#@login_required
def login(request):
    print("hello login")
    return render(request, 'waterDropApp/login.html',{})
