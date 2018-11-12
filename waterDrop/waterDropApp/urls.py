from django.urls import path
from django.contrib import admin
from . import views
admin.site.site_title = '管理画面'
admin.site.site_header = 'ウォータードロップ'
admin.site.index_title = 'メニュー'

urlpatterns = [
    path('', views.timeCard, name='timeCard'),
    path('timeCard/', views.timeCard, name='timeCard'),
    path('timeCardEntry/', views.timeCardEntry, name='timeCardEntry'),
    path('waterDropApp/', views.main, name='main'),
    path('mail/', views.mail, name="mail"),
    path(r'create_complete/.*', views.create_complete, name='create_complete')
]