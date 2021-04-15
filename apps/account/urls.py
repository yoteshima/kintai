# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('', views.top, name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]