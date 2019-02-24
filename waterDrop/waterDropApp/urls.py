from django.urls import path
from django.contrib import admin
from . import views
admin.site.site_title = '管理画面'
admin.site.site_header = 'ウォータードロップ'
admin.site.index_title = 'メニュー'

urlpatterns = [
    path('', views.main, name='main'),
    path('time_card/<str:code>', views.time_card, name='time_card'),
    path('work_content/<str:code>/<str:date>', views.work_content, name='work_content'),
    path('waterDropApp/', views.main, name='main'),
    path('mail/', views.mail, name="mail"),
    path(r'create_complete/', views.create_complete, name='create_complete')
]