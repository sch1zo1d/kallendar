from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import JsonResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, UserAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from .models import Event
from .utils import get_month, now_index
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def event_render_to_str(context, user):
    context['today_events_list'] = Event.objects.filter(user=user)
    context["html"] = render_to_string('cal/events.html', context)
    context.pop('today_events_list')
    return context


month_names = {'январь': '1', 'февраль': '2', 'март': '3', 'апрель': '4', 'май': '5', 'июнь': '6',
               'июль': '7', 'август': '8', 'сентябрь': '9', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'}


@login_required(login_url='cal:signup')
def index(request, year=None, month=None):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST" and is_ajax(request):
        nav = request.POST.get('nav')
        context = get_month(int(request.POST.get('current_year')), request.POST.get(
            'current_month'), nav)
        special_dates(context, user)
        context["html"] = render_to_string('cal/calendar.html', context)
        return JsonResponse(context)
    context = get_month()
    special_dates(context, user)
    context['today_events_list'] = Event.objects.filter(user=user)
    return render(request, 'cal/index.html', context)


def special_dates(context, user):
    if not Event.objects.filter(user=user):
        return
    current_year = context.get('current_year')
    c_month_index = context.get('c_month_index')

    current_month = datetime(current_year, c_month_index+1, 1)
    previous_month = current_month.replace(day=1) - timedelta(days=4)
    next_month = current_month.replace(day=28) + timedelta(days=4)

    prev_special_dates = get_sorted_special_month_dates(previous_month, user)
    now_special_dates = get_sorted_special_month_dates(current_month, user)
    next_special_dates = get_sorted_special_month_dates(next_month, user)

    context["prev_special_dates"] = get_current_special_dates(
        context.get('prev_dates'), prev_special_dates)
    context["special_dates"] = now_special_dates
    context["next_special_dates"] = get_current_special_dates(
        context.get('next_dates'), next_special_dates)
    # get_other_special_dates(context.get('prev_dates'),
    #                         context.get('next_dates'),
    #                         )
    # print(context.get('prev_dates'), context.get('next_dates'))
    # [i.date.day for i in list(Event.objects.filter(
    #     date__year=context.get('current_year'), date__month=context.get('c_month_index')+1, user=user))]
    # context.get('prev_dates')
    # print(context.get('current_year'), context.get('c_month_index')+1)

    return context


def get_current_special_dates(dates, current_dates):
    array = []
    for i in dates:
        if i in current_dates:
            array.append(i)
    return array


def get_sorted_special_month_dates(date, user):
    return sorted([i.date.day for i in list(Event.objects.filter(
        date__year=date.year, date__month=date.month, user=user))])


def delete_event(request):
    user = User.objects.get(pk=request.user.id)
    event = get_object_or_404(Event, pk=request.POST.get('id'))
    event.delete()
    return JsonResponse(event_render_to_str({}, user))


def all_events(request):
    user = User.objects.get(pk=request.user.id)
    return JsonResponse(event_render_to_str({}, user))


def today_event(request):
    user = User.objects.get(pk=request.user.id)
    date_str = '-'.join([request.POST.get('current_year'),
                        month_names[request.POST.get('current_month')], request.POST.get('current_day')])
    date = datetime.strptime(date_str, '%Y-%m-%d')
    # e = Event.objects.filter(date=date).order_by('-pub_date')
    context = {'today_events_list': Event.objects.filter(
        date=date, user=user), 'current_date': date}
    context["html"] = render_to_string('cal/events.html', context)
    context.pop('today_events_list')
    # print(Event.objects.filter(user=))
    return JsonResponse(context)
    # return JsonResponse(event_render_to_str({}, get_list_or_404(Event, date=request.POST.get('date'))))


def add_event(request):
    d = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
    context = {
        'tittle': request.POST.get('tittle'),
        'notes': request.POST.get('notes'),
        'date': request.POST.get('date'),
        'time': request.POST.get('time'),
        'current_date': d,
    }
    user = User.objects.get(pk=request.user.id)
    if not context.get('time'):
        context['time'] = None
    # date = datetime.strptime(context.get('date'), '%-%m-%d')
    tom = Event(user=user, tittle=context.get('tittle'), notes=context.get(
        'notes'), date=context.get('date'), time=context.get('time'))
    tom.save()
    context['today_events_list'] = Event.objects.filter(
        date=d, user=user)
    context["html"] = render_to_string('cal/events.html', context)
    context.pop('today_events_list')
    return JsonResponse(context)


def edit_event(request, event_id):
    pass


def signup(request):
    if request.method == "POST":
        req = request.POST.get('submit')
        if req == 'sign_in':  # Вход
            username_or_email = request.POST.get("username")
            password = request.POST.get("password1")
            try:
                validate_email(username_or_email)
            except ValidationError:
                user = authenticate(
                    username=username_or_email, password=password)
            else:
                username_or_email = User.objects.get(email=username_or_email)
                user = authenticate(
                    username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect("cal:index")
        elif req == 'sign_up':  # Регистрация
            username = request.POST.get("username")
            email = request.POST.get('email')
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 == password2:
                User.objects.create_user(
                    username=username, email=email, password=password1)
                user = authenticate(username=username, password=password1)
                login(request, user)
                return redirect("cal:index")
            else:
                return render(request, 'signup.html', {'err': 'Пароли не совпадают'})
    return render(request, 'signup.html')


def validate_username(request):
    """Check username availability"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def journal(request):
    return render(request, 'cal/journal.html')
# def all_events(request):
#     all_events = Event.objects.all()
#     out = []
#     for event in all_events:
#         out.append({
#             'title': event.title,
#             'id': event.id,
#             'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
#             'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"), })
#     return JsonResponse(out, safe=False)


# def add_event(request):
#     start = request.GET.get("start", None)
#     end = request.GET.get("end", None)
#     title = request.GET.get("title", None)
#     event = Event(title=str(title), start=start, end=end)
#     event.save()
#     data = {}
#     return JsonResponse(data)


# def update(request):
#     start = request.GET.get("start", None)
#     end = request.GET.get("end", None)
#     title = request.GET.get("title", None)
#     id = request.GET.get("id", None)
#     event = Event.objects.get(id=id)
#     event.start = start
#     event.end = end
#     event.title = title
#     event.save()
#     data = {}
#     return JsonResponse(data)


def hello(request):
    context = {
        'res': request.POST.get("current_year", None)
    }
    return JsonResponse(context)
# class RegisterView(FormView):
#     form_class = RegisterForm
#     template_name = 'signup.html'
#     success_url = reverse_lazy("cal:index")

#     def form_valid(self, form):
#         form.save()
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         return redirect("cal:index")
#         return super().form_valid(form)
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Регистрация")
#         return dict(list(context.items())+list(c_def.items()))


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy("cal:index")

    def get(self, requset):
        return render(requset, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("cal:index")
            # return super().form_valid(form)
        return render(request, self.template_name, {'form': form})


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
