# -*- coding: utf-8 -*-

"""
    時間表示に関わる関数
"""
from datetime import datetime, timedelta

def sum_time(time_strings):
    """
        時間の合計を計算します
    """
    today = datetime.today()
    base_time = datetime(year=today.year, month=today.month, day=1)
    datetimes = [(convert_to_datetime(time_string).replace(day=1) - base_time).total_seconds() for time_string in time_strings]
    total_seconds = sum(datetimes)

    hour = str(int(total_seconds/3600)).zfill(1)
    second = str(int(total_seconds%3600/60)).zfill(2)

    return f"{hour}:{second}"


def convert_to_datetime(string_time):
    """
        str型の時間データをdatetime型に直します
    """
    SEPARATOR = ":"

    today = datetime.today()
    trimmed_string_time = string_time.replace(" ","").zfill(4)

    if SEPARATOR in trimmed_string_time:
        hour,minute = [int(num) for num in trimmed_string_time.split(SEPARATOR)]

    elif len(trimmed_string_time) == 4:
        hour = int(trimmed_string_time[:2])
        minute = int(trimmed_string_time[2:])

    if minute != None and minute < 60:
        converted_time = datetime(
            year = today.year,
            month = today.month,
            day = today.day,
            hour = hour%24,
            minute = minute,
        ) + timedelta(days=hour//24)

        return converted_time


def convert_to_clock_time(string_time):
    """
        時間入力値を変換します。
    """
    if string_time:
        FLOAT_SEPARATORS = ".．,、"
        TIME_SEPARATORS = ":;：；"

        hour_num, minute_num = "", ""
        float_flg, time_flg = False, False
        is_negative = False

        try:
            if string_time[0] == "-":
                is_negative = True
                string_time = string_time[1:]

            if string_time.isnumeric() and len(string_time) == 4:
                int_hour = int(string_time[:2])
                int_minute = int(string_time[2:])
                hour,minute = round_up_time(int_hour,int_minute)

            else:
                for c in string_time:
                    if c.isnumeric():
                        if not time_flg and not float_flg:
                            hour_num += c
                        else:
                            minute_num += c

                    elif c in FLOAT_SEPARATORS:
                        if time_flg or float_flg:
                            raise
                        float_flg = True

                    elif c in TIME_SEPARATORS:
                        if time_flg or float_flg:
                            raise
                        time_flg = True

                int_hour = int(hour_num)
                if time_flg:
                    int_minute = int(minute_num)
                else:
                    int_minute = int(float("0." + minute_num)*60)

                hour,minute = round_up_time(int_hour,int_minute)

            if is_negative:
                hour = "-" + str(hour)

            clock_time = f"{hour}:{minute}"

            return clock_time

        except Exception as e:
            pass

def round_up_time(hour,minute):
    """
        時間を15分区切りで切り上げます
    """
    if minute % 15:
        round = (minute//15 + 1)
        minute = round * 15

    if minute >= 60:
        round = (minute//60)
        minute = minute - round * 60
        hour += round

    return str(hour),str(minute).zfill(2)


def convert_to_float_time(string_time):
    """
        時間入力値を変換します。
    """
    if string_time:
        FLOAT_SEPARATORS = ".．,、"
        TIME_SEPARATORS = ":;：；"

        int_num, dec_num = "", ""
        float_flg, time_flg = False, False

        try:
            for c in string_time:
                if c.isnumeric():
                    if not time_flg and not float_flg:
                        int_num += c
                    else:
                        dec_num += c

                elif c in FLOAT_SEPARATORS:
                    if time_flg or float_flg:
                        raise
                    float_flg = True

                elif c in TIME_SEPARATORS:
                    if time_flg or float_flg:
                        raise
                    time_flg = True

            if time_flg:
                float_time = float(int(int_num) + int(dec_num) / 60)
            else:
                float_time = float(int_num + "." + dec_num)

            return round(float_time,2)

        except Exception as e:
            pass

    else:
        return 0

def convert_to_serial_time(string_time):
    """
        HH:MM形式の時間表記をexcelのシリアル時間に変換します。
        また、0:00の時はブランクにします。
    """
    if type(string_time) == str and len(string_time.split(":")) == 2 and all([i.isnumeric() for i in string_time.split(":")]):
        split_time = [int(i) for i in string_time.split(":")]
        if sum(split_time) == 0:
            return ""
        else:
            return split_time[0]/24 + split_time[1]/24/60
