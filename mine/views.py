from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import mineDetail
from django.contrib.auth import authenticate,login,logout

def index(request):
    return render(request, 'index.html')

def calculator(request):
    return render(request, 'calculator.html')

@login_required
def livedash(request):
    return render(request, 'dashboard.html')

def customLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'dashboard.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def customLogout(request):
    logout(request)
    return redirect('index')