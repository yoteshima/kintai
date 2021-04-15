from django.contrib import admin
from apps.work_report.models import WorkReport, WorkDetail, Status, ReportSettings

admin.site.register(WorkReport)
admin.site.register(WorkDetail)
admin.site.register(Status)
admin.site.register(ReportSettings)
