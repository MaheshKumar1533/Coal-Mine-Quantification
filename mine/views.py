from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import mineDetail,fueltype, explosion,mineaddress,emissions
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

def index(request):
    return render(request, 'index.html')

def calculator(request):
    return render(request, 'calculator.html')

@login_required
def livedash(request):

    emission  = emissions.objects.get(mine=request.user)
    print(emission)
    return render(request, 'dashboard.html', {
        'emissions': emission,
    })

def customLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('admindash')
            return render(request, 'dashboard.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def customLogout(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if password == confirm_password:
            try:
                # Create the user (mineDetail)
                user = mineDetail.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=firstname
                )
                user.save()
                emission = emission.objects.create(mine=user)
                emission.save()

                # Store the user's ID in the session and proceed to the next step
                request.session['user_id'] = user.id
                return redirect('register_step2')

            except Exception as e:
                error_message = f'An error occurred: {str(e)}'
        else:
            error_message = 'Passwords do not match'

        return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')




def register_step2(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('register_step1')

    user = mineDetail.objects.get(id=user_id)

    if request.method == 'POST':
        # mineDetail information
        coal_type = request.POST.get('coal_type', 'UnderGround')
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

        # mineaddress information
        street_address = request.POST.get('street_address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()
        country = request.POST.get('country', 'India').strip()
        latitude_address = request.POST.get('latitude_address', 0).strip()
        longitude_address = request.POST.get('longitude_address', 0).strip()

        # Update mineDetail fields
        user.coal_type = coal_type
        user.area = float(area) if area else 0.0
        user.green_area = float(green_area) if green_area else 0.0
        user.mine_area = float(mine_area) if mine_area else 0.0
        user.bare_land = bool(bare_land)
        user.save()

        # Create fueltype record
        fuel = fueltype(username=user, transport=transport, toolUsage=toolUsage)
        fuel.save()

        # Create explosion record
        explosion_record = explosion(username=user, explosiveType=explosiveType, emissionFactor=float(emissionFactor) if emissionFactor else 0.0)
        explosion_record.save()

        # Create mineaddress record
        address = mineaddress(
            username=user,
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            latitude=float(latitude_address) if latitude_address else 0.0,
            longitude=float(longitude_address) if longitude_address else 0.0
        )
        address.save()

        # Clear the session and log in the user
        del request.session['user_id']
        login(request, user)
        return redirect('livedash')

    return render(request, 'register_step2.html')

def initiatives(request):
    return render(request, 'initiatives.html')



@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        # Updating mineDetail information
        user.first_name = request.POST.get('firstname', user.first_name).strip()
        user.username = request.POST.get('username', user.username).strip()
        user.email = request.POST.get('email', user.email).strip()
        user.coal_type = request.POST.get('coal_type', user.coal_type)
        user.latitude = request.POST.get('latitude', user.latitude)
        user.longitude = request.POST.get('longitude', user.longitude)
        user.area = request.POST.get('area', user.area)
        user.green_area = request.POST.get('green_area', user.green_area)
        user.mine_area = request.POST.get('mine_area', user.mine_area)
        user.bare_land = request.POST.get('bare_land', user.bare_land)
        
        # Save mineDetail
        user.save()

        # Updating fueltype information
        fuel = fueltype.objects.get(username=user)
        fuel.transport = request.POST.get('transport', fuel.transport)
        fuel.toolUsage = request.POST.get('toolUsage', fuel.toolUsage)
        fuel.save()

        # Updating explosion information
        explosion_record = explosion.objects.get(username=user)
        explosion_record.explosiveType = request.POST.get('explosiveType', explosion_record.explosiveType)
        explosion_record.emissionFactor = request.POST.get('emissionFactor', explosion_record.emissionFactor)
        explosion_record.save()

        # Updating mineaddress information
        address = mineaddress.objects.get(username=user)
        address.street_address = request.POST.get('street_address', address.street_address).strip()
        address.city = request.POST.get('city', address.city).strip()
        address.state = request.POST.get('state', address.state).strip()
        address.zip_code = request.POST.get('zip_code', address.zip_code).strip()
        address.country = request.POST.get('country', address.country).strip()
        address.latitude = request.POST.get('latitude_address', address.latitude)
        address.longitude = request.POST.get('longitude_address', address.longitude)
        address.save()

        # If the user changed their password, update it and re-authenticate
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password and password == confirm_password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)

        return redirect('profile')

    # Get the user's existing data for rendering
    fuel = fueltype.objects.get(username=user)
    explosion_record = explosion.objects.get(username=user)
    address = mineaddress.objects.get(username=user)

    context = {
        'user': user,
        'fuel': fuel,
        'explosion_record': explosion_record,
        'address': address
    }
    return render(request, 'profile.html', context)

def admindash(request):
    mines = mineDetail.objects.exclude(username = "ministryofcoal")
    details = []
    total_emissions = 0
    for mine in mines:
        address = mineaddress.objects.get(username=mine).state
        emission = emissions.objects.get(mine=mine).total_emissions
        total_emissions += emission

        details.append({
            "name": mine.first_name,
            "state": address,
            "type": mine.coal_type,
            "emission": emission,
            "area": mine.area,
        })
    return render(request, 'admindash.html',{
        "mine_count": len(mines),
        "total_emissions": total_emissions,
        "details": details
    })