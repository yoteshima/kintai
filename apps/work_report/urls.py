# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views



app_name = 'work_report'

urlpatterns = [
    path('work_report/', views.show_work_report, name='work_report'),
    path('time_stamp/', views.show_time_stamp, name='time_stamp'),
    path('settings/', views.show_settings, name='settings'),

    path('export_excel/', views.export_excel, name='export_excel'),
    path('reset_report/', views.reset_report, name='reset_report'),

    re_path(r'^.*/*exec/$', views.exec_ajax, name='exec'),

]