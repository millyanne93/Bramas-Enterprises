from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .models import Car, UserProfile, Booking
from .forms import BookingForm, CustomUserCreationForm, UserProfileForm
from django.http import JsonResponse, HttpResponseRedirect
from car_dealer.models import *
from django.http import HttpResponseBadRequest
from django.http import HttpResponse


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/registration/login.html')
    else:
        return render(request, 'customer/home.html')

def home(request):
    return render(request, 'customer/home.html')

class CustomLogoutView(LogoutView):
    next_page = 'customer/home'

def base(request):
    return render(request, 'customer/base.html', {'name': 'Customer'})

def about(request):
    return render(request, 'customer/about.html')

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Account created successfully')
            return redirect('customer/registration/login.html')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'customer/registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def get_user_data(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    if user_profile:
        data.update({
            'phone_number': user_profile.phone_number,
            'address': user_profile.address,
            'location': user_profile.location.name,
        })
    return JsonResponse(data)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'customer/registration/login.html')
    else:
        return render(request, 'customer/registration/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def search(request):
    if request.method == 'POST':
        city = request.POST['city'].lower()
        cars_list = []
        location = Location.objects.filter(city=city)
        for l in location:
            cars = Cars.objects.filter(location=l, is_available=True)
            for car in cars:
                car_dictionary = {
                    'name': car.car_name,
                    'year': car.year,
                    'make': car.make,
                    'id': car.id,
                    'pincode': car.location.pincode,
                    'capacity': car.capacity,
                    'description': car.description
                }
                cars_list.append(car_dictionary)
        return render(request, 'customer/search_results.html', {'cars_list': cars_list})
    return render(request, 'customer/search.html')

@login_required
def rent_car(request):
    try:
        id = request.POST['id']
        car = get_object_or_404(Car, id=id)
        cost_per_day = int(car.capacity) * 13
        return render(request, 'confirmation.html', {'car': car, 'cost_per_day': cost_per_day})
    except (KeyError, Car.DoesNotExist):
        return HttpResponse("Invalid car ID or missing data.")

@login_required
def confirm(request):
    if request.method == "POST":
        car_id = request.POST.get('id')
        rent = request.POST.get('rent')
        user = request.user
        if car_id is None or rent is None:
            return HttpResponseBadRequest("Missing 'id' or 'rent' parameter")
        try:
            car = Cars.objects.get(id=car_id)
            if car.is_available:
                car_dealer = car.dealer
                days = 1
                rent = int(car.capacity) * 13 * days
                car_dealer.wallet += rent
                car_dealer.save()

                booking = Bookings.objects.create(
                    car=car,
                    car_dealer=car_dealer,
                    user=user,
                    rent=rent,
                    days=days
                )
                car.is_available = False
                car.save()
                return render(request, 'customer/confirmed.html', {'booking': booking})
            else:
                return render(request, 'customer/order_failed.html')
        except Cars.DoesNotExist:
            return HttpResponseBadRequest("Invalid car ID")
    else:
        return HttpResponseBadRequest("Invalid request method. Please submit the form.")

@login_required
def manage(request):
    booking_list = []
    user = request.user
    bookings = Booking.objects.filter(user=user, is_complete=False)
    for booking in bookings:
        booking_dictionary = {
            'id': booking.id,
            'rent': booking.rent,
            'car': booking.car,
            'days': booking.days,
            'car_dealer': booking.car_dealer
        }
        booking_list.append(booking_dictionary)
    return render(request, 'customer/manage.html', {'bookings': booking_list})

@login_required
def update_order(request):
    booking_id = request.POST['id']
    booking = Booking.objects.get(id=booking_id)
    car = booking.car
    car.is_available = True
    car.save()
    car_dealer = booking.car_dealer
    car_dealer.wallet -= int(booking.rent)
    car_dealer.save()
    booking.delete()
    cost_per_day = int(car.capacity) * booking.days
    return render(request, 'customer/confirmation.html', {'car': car, 'cost_per_day': cost_per_day})

@login_required
def delete_order(request):
    booking_id = request.POST['id']
    booking = Bookings.objects.get(id=booking_id)
    car_dealer = booking.car_dealer
    car_dealer.wallet -= int(booking.rent)
    car_dealer.save()
    car = booking.car
    car.is_available = True
    car.save()
    booking.delete()
    return HttpResponseRedirect('manage')
