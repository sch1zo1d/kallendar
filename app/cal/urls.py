from django.conf import settings
from django.urls import path, include
from . import views
from .views import RegisterView, UserLoginView
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView

app_name = 'cal'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.signup, name='signup'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('validate_username', views.validate_username, name='validate_username'),
    # path('other_month', views.get_other_month, name="other_month")
    # path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # path('register', RegisterView.as_view(), name='register'),
    # path('login', UserLoginView.as_view(), name='login'),
    # path('api/register/', CreateUserView.as_view(), name='register'),

    # path('', include("django.contrib.auth.urls")),
    # path('signup', views.SignUpView.as_view(), name='signup'),
    # path('<int:year>/<int:month>/<int:day>', views.date, name='date'),
    # # # ex: /polls/5/results/
    # # path('<int:question_id>/results/', views.results, name='results'),
    # # # ex: /polls/5/vote/
    # # path('<int:question_id>/vote/', views.vote, name='vote'),
    # # https://calendar.google.com/calendar/u/0/r/day/2023/2/7?pli=1
    # path('cal/<int:event_id>/', views.detail, name='detail'),
    # # path('ajax/info_getter/', views.info_getter, name='info_getter'),
    # # ex: /polls/5/results/
    # path('<int:event_id>/events/', views.results, name='results'),
    # ex: /polls/5/vote/
]
