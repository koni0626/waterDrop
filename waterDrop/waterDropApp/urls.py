from django.urls import path
from django.contrib import admin
from . import views
admin.site.site_title = '管理画面'
admin.site.site_header = 'ウォータードロップ'
admin.site.index_title = 'メニュー'

urlpatterns = [
    path('', views.main, name='main'),
    path('waterDropApp/', views.main, name='main'),
]