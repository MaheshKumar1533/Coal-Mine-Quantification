from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def calculator(request):
    return render(request, 'calculator.html')

def livedash(request):
    return render(request, 'dashboard.html')
