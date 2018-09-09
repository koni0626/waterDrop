from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('waterDropApp/', views.main, name='main'),
]