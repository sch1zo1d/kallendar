from .models import *
from django.db.models import Count
from calendar import isleap, weekday
from datetime import datetime
now = datetime.now()


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

def get_month(year=now.year, month=now.month):
    month_names = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                   'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    current_month = month_names[month-1]
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_now = days_in_month[month-1]
    days_in_prev = days_in_month[month-2]
    if days_in_now == 28 and isleap(year):
        days_in_now = 29
    prev_dates = [i for i in range(
        days_in_prev - weekday(year, month, 1)+1, days_in_prev+1)]
    now_dates = [i for i in range(1, days_in_now+1)]
    next_dates = [i for i in range(
        1, 1 + len(range((len(prev_dates)+len(now_dates)), 42)))]
    return prev_dates, now_dates, next_dates, current_month, year
