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

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import mineDetail, fueltype, explosion

def register(request):
    if request.method == 'POST':
        # User information
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # mineDetail information
        coal_type = request.POST.get('coal_type', 'UnderGround')
        latitude = request.POST.get('latitude', 0).strip()
        longitude = request.POST.get('longitude', 0).strip()
        area = request.POST.get('area', 0).strip()
        green_area = request.POST.get('green_area', 0).strip()
        mine_area = request.POST.get('mine_area', 0).strip()
        bare_land = request.POST.get('bare_land', False)

        # fueltype information
        transport = request.POST.get('transport', 'Diesel')
        toolUsage = request.POST.get('toolUsage', 'Diesel')

        # explosion information
        explosiveType = request.POST.get('explosiveType', '').strip()
        emissionFactor = request.POST.get('emissionFactor', 0).strip()

        if password == confirm_password:
            try:
                # Create the user (mineDetail)
                user = mineDetail.objects.create_user(username=username, password=password)
                
                # Set mineDetail fields only if they are not empty
                user.coal_type = coal_type
                user.latitude = float(latitude) if latitude else 0.0
                user.longitude = float(longitude) if longitude else 0.0
                user.area = float(area) if area else 0.0
                user.green_area = float(green_area) if green_area else 0.0
                user.mine_area = float(mine_area) if mine_area else 0.0
                user.bare_land = bool(bare_land)

                user.save()

                # Create fueltype record if values are provided
                if transport or toolUsage:
                    fuel = fueltype(username=user, transport=transport, toolUsage=toolUsage)
                    fuel.save()

                # Create explosion record if values are provided
                if explosiveType or emissionFactor:
                    explosion_record = explosion(username=user, explosiveType=explosiveType, emissionFactor=float(emissionFactor) if emissionFactor else 0.0)
                    explosion_record.save()

                login(request, user)
                return redirect('livedash')
            except Exception as e:
                error_message = f'An error occurred: {str(e)}'
        else:
            error_message = 'Passwords do not match'

        return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')


def initiatives(request):
    return render(request, 'initiatives.html')