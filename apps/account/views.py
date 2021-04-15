from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

from .forms import LoginForm


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'register/top.html' 

def top(request):
    # return render(request, 'register/top.html', {'user': request.user})
    return render(request, 'time_stamp/time_stamp.html', {'user': request.user})