from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, UserAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from .models import Event
from .utils import get_month
from django.contrib.auth.decorators import login_required


@login_required(login_url='accounts/login/')
def index(request, year=None, month=None):
    # if year == None:
    # else:
    # prev_dates, now_dates, next_dates, с_month, c_year = get_month(year, month)
    # latest_event_list = Event.objects.order_by('-pub_date')[:5]
    if request.method == "GET":
        prev_dates, now_dates, next_dates, с_month, c_year = get_month()
    elif request.method == "POST":
        if request.POST.get('nav') == 'next':
            navigate = 'next'
        elif request.POST.get('nav') == 'prev':
            navigate = 'prev'
        prev_dates, now_dates, next_dates, с_month, c_year = get_month(int(
            request.POST.get('current_year')), request.POST.get('current_month'), navigate)
        context = {
            # 'latest_event_list': latest_event_list,
            'prev_dates': prev_dates,
            'now_dates': now_dates,
            'next_dates': next_dates,
            'current_month': с_month,
            'current_year': c_year,
        }
        return JsonResponse(context)
    context = {
        # 'latest_event_list': latest_event_list,
        'prev_dates': prev_dates,
        'now_dates': now_dates,
        'next_dates': next_dates,
        'current_month': с_month,
        'current_year': c_year,
    }
    return render(request, 'cal/index.html', context)


# def get_other_month(request):
#     if request.POST.get('nav') == 'next':
#         navigate = 'next'
#     elif request.POST.get('nav') == 'prev':
#         navigate = 'prev'
#     prev_dates, now_dates, next_dates, с_month, c_year = get_month(int(request.POST.get('current_year')), request.POST.get('current_month'), navigate)
#     context = {
#         # 'latest_event_list': latest_event_list,
#         'prev_dates': prev_dates,
#         'now_dates': now_dates,
#         'next_dates': next_dates,
#         'current_month': с_month,
#         'current_year': c_year,
#     }
#     return JsonResponse(context)


def signup(request):
    if request.method == "POST":
        req = request.POST.get('submit')
        if req == 'sign_in':  # Вход
            username = request.POST.get("username")
            password = request.POST.get("password1")
            user = authenticate(username=username, password=password)
            print(req, user)
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


def all_events(request):
    all_events = Event.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.title,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"), })
    return JsonResponse(out, safe=False)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Event(title=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.start = start
    event.end = end
    event.title = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)




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
