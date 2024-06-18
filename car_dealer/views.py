from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Car, CarDealer, Location
from .forms import CarForm, CarDealer
from car_rental.models import Booking
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


def base(request):
    return render(request, 'owner/base.html')

# Index
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'owner/login.html')
    else:
        return render(request, 'owner/home.html')

def home(request):
        return render(request, 'owner/home.html')

class CarDealerLoginView(View):
    def get(self, request):
        return render(request, 'owner/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change 'home' to the appropriate URL name for the home page
        else:
            return render(request, 'owner/login_failed.html')

def logout_view(request):
    logout(request)
    return render(request, 'owner/login.html')

def register(request):
    return render(request, 'owner/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password'] 
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    mobile = request.POST['mobile']
    pincode = request.POST['pincode']
    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'owner/registration_error.html')
    try:
        location = Location.objects.get(city = city, pincode = pincode)
    except:
        location = None
        if location is not None:
            car_dealer = CarDealer(car_dealer = user, mobile = mobile, location=location)
    else:
        location = Location(city = city, pincode = pincode)
        location.save()
        location = Location.objects.get(city = city, pincode = pincode)
        car_dealer = CarDealer(car_dealer = user, mobile = mobile, location=location)
    car_dealer.save()
    return render(request, 'owner/registration_succesful.html')
# Add Vehicle
@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.dealer = request.user.cardealer  # Assuming the user is linked to CarProvider
            car.save()
            messages.success(request, 'Vehicle added successfully')
            return redirect('manage_vehicles')
        else:
            form = CarForm()
        return render(request, 'owner/add_car.html', {'form': form})
# Manage Vehicles
@login_required
def manage_cars(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    car_list = []
    cars = Cars.objects.filter(dealer = car_dealer)
    for c in cars:
        car_list.append(c)
        return render(request, 'owner/manage.html', {'car_list':car_list})
# View Order List
@login_required
def view_booking_list(request):
    try:
        cardealer = request.user.cardealer
    except ObjectDoesNotExist:
        return HttpResponse("You are not associated with any car dealer.", status=404)

    bookings = Booking.objects.filter(car__dealer=request.user.cardealer, is_complete=False)
    return render(request, 'owner/booking_list.html', {'bookings': bookings})
# Complete Order
@login_required
def complete_booking(request, order_id):
    booking = get_object_or_404(Booking, id=order_id, car__dealer=request.user.cardealer)
    booking.is_complete = True
    booking.car.is_available = True
    booking.car.save()
    booking.save()
    messages.success(request, 'Booking marked as complete')
    return redirect('owner/booking_list')
# Order History
@login_required
def booking_history(request):
    bookings = Booking.objects.filter(car__dealer=request.user.cardealer)
    wallet = sum(booking.rent for booking in bookings)
    return render(request, 'owner/booking_history.html', {'bookings': bookings})
# Delete Vehicle
@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, dealer=request.user.cardealer)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Vehicle deleted successfully')
        return HttpResponseRedirect('owner/manage_cars')
