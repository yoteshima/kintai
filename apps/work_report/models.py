from django.db import models
from django.utils import timezone

import uuid
from datetime import datetime

from . import time_util

class WorkReport(models.Model):
    report_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_period = models.DateField(auto_now=False, auto_now_add=False)
    project_name = models.TextField(blank=True, null=True, default="")
    site_work_time = models.TextField(blank=True, null=True, default="0:00")
    user_id = models.ForeignKey("account.User", to_field="no", on_delete=models.PROTECT)

    @property
    def report_total_time(self):
        work_details = WorkDetail.objects.filter(report_no = self.report_no)
        total_times = [work_detail.total_time for work_detail in work_details]
        total_time = time_util.sum_time(total_times)
        return total_time

    @property
    def report_mean_time(self):
        work_details = WorkDetail.objects.filter(report_no = self.report_no)
        total_times = [work_detail.mean_time for work_detail in work_details]
        mean_time = time_util.sum_time(total_times)
        return mean_time

    @property
    def report_over_time(self):
        work_details = WorkDetail.objects.filter(report_no = self.report_no)
        total_times = [work_detail.over_time for work_detail in work_details]
        over_time = time_util.sum_time(total_times)
        return over_time

    @property
    def report_midnight_over_time(self):
        work_details = WorkDetail.objects.filter(report_no = self.report_no)
        total_times = [work_detail.midnight_over_time for work_detail in work_details]
        midnight_over_time = time_util.sum_time(total_times)
        return midnight_over_time

    @property
    def report_holiday_work(self):
        work_details = WorkDetail.objects.filter(report_no = self.report_no)
        total_times = [work_detail.holiday_work for work_detail in work_details]
        holiday_work = time_util.sum_time(total_times)
        return holiday_work

    @property
    def work_days(self):
        work_details = WorkDetail.objects.filter(report_no = self.report_no)
        week_days_date = [work_detail for work_detail in work_details if (work_detail.work_date.weekday() not in (5,6) or int(work_detail.status.code) in (11,8)) and int(work_detail.status.code) not in (1,2,3,4,9,10,12,13)]
        return len(week_days_date)

    @property
    def holidays(self):
        work_details = WorkDetail.objects.filter(report_no = self.report_no)
        holidays_date = [work_detail for work_detail in work_details if (work_detail.work_date.weekday() in (5,6) and int(work_detail.status.code) not in (11,8)) or int(work_detail.status.code) in (1,2,3,4,9,10,12,13)]
        return len(holidays_date)

    @property
    def diff_total_time(self):
        site_work_time = time_util.convert_to_float_time(self.site_work_time)
        report_mean_time = time_util.convert_to_float_time(self.report_mean_time)
        diff_time = time_util.convert_to_clock_time(str(report_mean_time - site_work_time))
        return diff_time

    def __str__(self):
        return f"{self.report_period.strftime('%Y-%m')}_{self.user_id}"

class WorkDetail(models.Model):
    serial_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_no = models.ForeignKey("WorkReport", to_field="report_no", on_delete=models.PROTECT)
    work_date = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.TextField(blank=True, null=True, default="0:00")
    end_time = models.TextField(blank=True, null=True, default="0:00")
    break1 = models.FloatField(blank=True, null=True, default=0)
    break2 = models.FloatField(blank=True, null=True, default=0)
    start_break = models.TextField(blank=True, null=True, default="12:00")
    end_break = models.TextField(blank=True, null=True, default="13:00")
    status = models.ForeignKey("Status", to_field="code", on_delete=models.PROTECT, default=0)
    remarks = models.TextField(blank=True, null=True, default="")

    @property
    def total_time(self):
        if (self.start_time and self.start_time != "0:00") and (self.end_time and self.end_time != "0:00"):
            try:
                today = datetime.today()

                # 初期化
                start_time = time_util.convert_to_datetime(self.start_time)
                end_time = time_util.convert_to_datetime(self.end_time)

                total_seconds = (end_time-start_time).total_seconds()
                hour = str(int(total_seconds/3600)).zfill(1)
                second = str(int(total_seconds%3600/60)).zfill(2)

                return f"{hour}:{second}"

            except:
                return ""
        else:
            return ""

    @property
    def mean_time(self):
        if (self.start_time and self.start_time != "0:00") and (self.end_time and self.end_time != "0:00"):
            try:
                today = datetime.today()

                total_time = time_util.convert_to_datetime(self.total_time)

                break1_time = time_util.convert_to_datetime(self.break1_time)
                break2_time = time_util.convert_to_datetime(self.break2_time)

                break_minute = (break1_time.hour + break2_time.hour)*60 + (break1_time.minute + break2_time.minute)
                total_break = datetime(
                    year=today.year, month=today.month, day=today.day, hour=break_minute//60, minute=break_minute%60
                )


                total_seconds = (total_time-total_break).total_seconds()
                hour = str(int(total_seconds/3600)).zfill(1)
                second = str(int(total_seconds%3600/60)).zfill(2)
                return f"{hour}:{second}"

            except:
                return ""
        else:
            return ""

    @property
    def over_time(self):
        try:
            today = datetime.today()

            mean_time = time_util.convert_to_datetime(self.mean_time)
            regular_time = datetime(
                year=today.year, month=today.month, day=today.day, hour=8, minute=0
            )

            total_seconds = (mean_time-regular_time).total_seconds()
            hour = str(int(total_seconds/3600)).zfill(1)
            second = str(int(total_seconds%3600/60)).zfill(2)

            if int(hour) > 0:
                return f"{hour}:{second}"

            else:
                return ""
        except:
            return ""

    @property
    def midnight_over_time(self):
        try:
            # if not self.over_time == "":

            today = datetime.today()

            end_time = time_util.convert_to_datetime(self.end_time)

            break2_time = time_util.convert_to_datetime(self.break2_time)
            midnight_break_seconds = break2_time.hour*3600 + break2_time.minute*60

            midnight_time = datetime(
                year=today.year, month=today.month, day=today.day, hour=22, minute=0
            )

            total_seconds = (end_time-midnight_time).total_seconds() - midnight_break_seconds
            hour = str(int(total_seconds/3600)).zfill(1)
            second = str(int(total_seconds%3600/60)).zfill(2)

            if int(hour) > 0:
                return f"{hour}:{second}"

            else:
                return ""
            # else:
                # return ""
        except:
            return ""

    @property
    def holiday_work(self):
        if self.status.code == 11:
            return self.total_time
        else:
            return ""

    @property
    def break1_time(self):
        total_seconds = self.break1 * 3600
        hour = str(int(total_seconds/3600)).zfill(1)
        second = str(int(total_seconds%3600/60)).zfill(2)

        if int(hour) or int(second):
            return f"{hour}:{second}"
        else:
            return ""

    @property
    def break2_time(self):
        total_seconds = self.break2 * 3600
        hour = str(int(total_seconds/3600)).zfill(1)
        second = str(int(total_seconds%3600/60)).zfill(2)

        if int(hour) or int(second):
            return f"{hour}:{second}"
        else:
            return ""

    @property
    def day_status(self):
        if (self.work_date.weekday() in (5,6) and self.status.code != 8) or self.status.code in (9,10):
            return "holiday"


    def __str__(self):
        return f"{self.work_date}_{self.report_no}"

class Status(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return f"{self.code}_{self.name}"

class ReportSettings(models.Model):
    serial_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey("account.User", to_field="no", on_delete=models.PROTECT)
    start_time = models.TextField(blank=True, null=True, default="9:00")
    end_time = models.TextField(blank=True, null=True, default="18:00")
    break1 = models.TextField(blank=True, null=True, default="1:00")
    break2 = models.TextField(blank=True, null=True, default="0:00")
    holidays = models.IntegerField(blank=True, null=True, default=96)
    project_name = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return f"{self.user_id}"

    @property
    def holiday_week(self):
        # WEEK = ["月","火","水","木","金","土","日"]
        WEEK = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        binary = bin(self.holidays)[2:]
        li = []

        count = 0
        for i in binary[-1::-1]:
            if i == "1" and count < len(WEEK):
                li.append(WEEK[count])
            count += 1

        return li