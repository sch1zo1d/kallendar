from .models import *
from django.db.models import Count
from calendar import isleap, weekday
from datetime import datetime
now = datetime.now()


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
    if isleap(int(c_year)):
        if days_in_now == 28:
            days_in_now = 29
        elif days_in_prev == 28:
            days_in_prev = 29
    prev_dates = [i for i in range(
        days_in_prev - weekday(c_year, c_month_index+1, 1)+1, days_in_prev+1)]
    now_dates = [i for i in range(1, days_in_now+1)]
    next_dates = [i for i in range(
        1, 1 + len(range((len(prev_dates)+len(now_dates)), 42)))]
    now_month = month_names[month_indexes.index(now.month)]
    return prev_dates, now_dates, next_dates, c_month, c_year, now.day, now_month, now.year
