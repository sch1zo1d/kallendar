from .models import *
from django.db.models import Count
from datetime import datetime
now = datetime.now()


def weekday(year: int, month: int, day: int) -> int:
    if month < 3:
        year -= 1
        month += 10
    else:
        month -= 2
    return (day + 31 * month // 12 + year + year // 4 - year // 100 + year // 400) % 7


def get_month(year=now.year, month=now.month, navigate=None):
    month_names = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                   'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    month_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    if type(month) == str:
        month_index = month_names.index(month)
    else:
        month_index = month_indexes.index(month)
    c_year = int(year)
    if navigate == "prev":
        if month_index == 0:
            c_year = year - 1
        c_month_index = month_names.index(month_names[month_index-1])
        c_month = month_names[c_month_index]
    elif navigate == "next":
        if month_index == 11:
            c_year = year + 1
            c_month_index = 0
            c_month = month_names[c_month_index]
        else:
            c_month_index = month_names.index(month_names[month_index+1])
            c_month = month_names[c_month_index]
    else:
        c_month_index = month_index
        c_month = month_names[month_index]
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_now = days_in_month[c_month_index]
    days_in_prev = days_in_month[c_month_index-1]
    if (c_year % 4 == 0 and c_year % 100 != 0) or c_year % 400 == 0:
        if days_in_now == 28:
            days_in_now = 29
        elif days_in_prev == 28:
            days_in_prev = 29
    prev_dates = [i for i in range(
        days_in_prev - weekday(c_year, c_month_index+1, 1)+2, days_in_prev+1)]
    now_dates = [i for i in range(1, days_in_now+1)]
    next_dates = [i for i in range(
        1, 1 + len(range((len(prev_dates)+len(now_dates)), 42)))]
    now_month = month_names[month_indexes.index(now.month)]
    return {
        'prev_dates': prev_dates,
        'now_dates': now_dates,
        'next_dates': next_dates,
        'current_month': c_month,
        'current_year': c_year,
        'now_day': now.day,
        'now_month': now_month,
        'now_year': now.year,
    }
