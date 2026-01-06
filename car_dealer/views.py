from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Car, CarDealer, Location
from .forms import CarForm
from car_rental.models import Booking
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

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

# UPDATED: Owner Login Function
def owner_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # CHECK IF USER IS ACTUALLY A CAR DEALER
            try:
                dealer = CarDealer.objects.get(car_dealer=user)
                # User is a car dealer, log them in
                login(request, user)
                return redirect('home')  # Owner home page
            except CarDealer.DoesNotExist:
                # User is not a car dealer, redirect to customer portal
                messages.error(request, 'This account is not registered as a car dealer. Please login as a customer.')
                return redirect('/car_rental/')
        else:
            return render(request, 'owner/login_failed.html')
    
    # GET request - show login form
    return render(request, 'owner/login.html')

# Remove or keep CarDealerLoginView for compatibility
class CarDealerLoginView(View):
    def get(self, request):
        return redirect('owner_login')  # Redirect to function-based view
    
    def post(self, request):
        return redirect('owner_login')  # Redirect to function-based view

def logout_view(request):
    logout(request)
    return render(request, 'owner/login.html')

def register(request):
    return render(request, 'owner/register.html')

# UPDATED: Registration function
def registration(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        city = request.POST['city'].lower()
        mobile = request.POST['mobile']
        pincode = request.POST['pincode']
        contact_info = request.POST.get('contact_info', '')

        # 1. Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'owner/registration_error.html', 
                         {'error': 'Username already exists. Please choose another.'})
        
        # 2. Create user
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname
            )
        except Exception as e:
            return render(request, 'owner/registration_error.html', 
                         {'error': f'Error creating user: {str(e)}'})

        # 3. Get or create location
        try:
            location, created = Location.objects.get_or_create(
                city=city,
                pincode=pincode,
                defaults={
                    'name': f"{city.title()} Branch",
                    'address': f"Main Street, {city.title()}"
                }
            )
        except Exception as e:
            # Clean up user if location fails
            user.delete()
            return render(request, 'owner/registration_error.html', 
                         {'error': f'Error creating location: {str(e)}'})

        # 4. Create car dealer profile
        try:
            car_dealer = CarDealer.objects.create(
                car_dealer=user,
                mobile=mobile,
                location=location,
                contact_info=contact_info if contact_info else f"{firstname} {lastname}"
            )
        except Exception as e:
            # Clean up user and location if car dealer fails
            user.delete()
            if created:  # Only delete location if we created it
                location.delete()
            return render(request, 'owner/registration_error.html', 
                         {'error': f'Error creating car dealer profile: {str(e)}'})

        # 5. Auto-login and redirect to owner portal
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        
        return render(request, 'owner/registered.html')

    # GET request - redirect to register form
    return redirect('register')

# Add Vehicle
@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                car = form.save(commit=False)
                car.dealer = request.user.cardealer
                car.save()
                messages.success(request, 'Vehicle added successfully')
                return redirect('manage_cars')
            except ObjectDoesNotExist:
                messages.error(request, 'You are not registered as a car dealer')
                return redirect('owner_login')
        else:
            form = CarForm()
        return render(request, 'owner/add_car.html', {'form': form})
    else:
        form = CarForm()
        return render(request, 'owner/add_car.html', {'form': form})

# UPDATED: Manage Vehicles with proper error handling
@login_required
def manage_cars(request):
    try:
        car_dealer = request.user.cardealer
        cars = Car.objects.filter(dealer=car_dealer)
        return render(request, 'owner/manage.html', {'car_list': cars})
    except ObjectDoesNotExist:
        messages.error(request, 'You are not registered as a car dealer')
        return redirect('owner_login')

# View Order List
@login_required
def view_booking_list(request):
    try:
        car_dealer = request.user.cardealer
        bookings = Booking.objects.filter(car__dealer=car_dealer, is_complete=False)
        return render(request, 'owner/booking_list.html', {'bookings': bookings})
    except ObjectDoesNotExist:
        return HttpResponse("You are not associated with any car dealer.", status=404)

# Complete Order
@login_required
def complete_booking(request, order_id):
    try:
        car_dealer = request.user.cardealer
        booking = get_object_or_404(Booking, id=order_id, car__dealer=car_dealer)
        booking.is_complete = True
        booking.car.is_available = True
        booking.car.save()
        booking.save()
        messages.success(request, 'Booking marked as complete')
        return redirect('booking_list')
    except ObjectDoesNotExist:
        messages.error(request, 'You are not registered as a car dealer')
        return redirect('owner_login')

# Order History
@login_required
def booking_history(request):
    try:
        car_dealer = request.user.cardealer
        bookings = Booking.objects.filter(car__dealer=car_dealer)
        wallet = sum(int(booking.rent) for booking in bookings if booking.rent)
        return render(request, 'owner/booking_history.html', {'bookings': bookings, 'wallet': wallet})
    except ObjectDoesNotExist:
        messages.error(request, 'You are not registered as a car dealer')
        return redirect('owner_login')

# Delete Vehicle
@login_required
def delete_car(request, car_id):
    try:
        car_dealer = request.user.cardealer
        car = get_object_or_404(Car, id=car_id, dealer=car_dealer)
        if request.method == 'POST':
            car.delete()
            messages.success(request, 'Vehicle deleted successfully')
            return redirect('manage_cars')
        return render(request, 'owner/confirm_delete.html', {'car': car})
    except ObjectDoesNotExist:
        messages.error(request, 'You are not registered as a car dealer')
        return redirect('owner_login')
