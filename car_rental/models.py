from django.db import models
from django.contrib.auth.models import User
from car_dealer.models import Car, Location, CarDealer

class Booking(models.Model):
    """
    A class representing a booking transaction in the car rental application.
    Attributes:
        user (ForeignKey): The user who made the booking.
        car (ForeignKey): The car being rented
        car_dealer (ForeignKey): The car dealer from which the car is rented.
        rental_date (DateField): The date when the rental period starts.
        return_date (DateField): The date when the rental period ends.
        pickup_location (CharField): The location where the car will be picked up.
        rental_days (PositiveIntegerField): The number of days the car is rented.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE, default=1)
    rent = models.CharField(max_length=8)
    days = models.IntegerField(default=1)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the rental transaction.

        Returns:
            str: A string containing information about the rented car and the renter.
        """
        return f"{self.car} rented by {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, default="Nairobi")

    def __str__(self):
        """
        Returns a string representation of the user profile.
        Returns:
            str: A string containing the username.
        """
        return self.user.username
