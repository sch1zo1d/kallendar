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
    if year == None:
        prev_dates, now_dates, next_dates, current_month, current_year = get_month()
    else:
        prev_dates, now_dates, next_dates, current_month, current_year = get_month(
            year, month)
    latest_event_list = Event.objects.order_by('-pub_date')[:5]
    weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    context = {
        # 'latest_event_list': latest_event_list,
        # 'weekdays': weekdays,
        # 'month_dates': month_dates,
        'prev_dates': prev_dates,
        'now_dates': now_dates,
        'next_dates': next_dates,
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(request, 'cal/index.html', context)


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
                return render(request, 'signup.html', {'err':'Пароли не совпадают'})
    return render(request, 'signup.html')


def validate_username(request):
    """Check username availability"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


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
