from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    pincode = models.CharField(
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],
        max_length=6,
        unique=True
    )
    city = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}, {self.city}, {self.pincode}"

class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=100)
    location = models.OneToOneField(Location, on_delete=models.PROTECT)
    wallet = models.IntegerField(default = 0)
    mobile = models.CharField(max_length=15, default='0000000000')

    def __str__(self):
        return self.name

class Car(models.Model):
    dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE, related_name='cars')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cars')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    capacity = models.CharField(max_length = 2)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='car_photos/', blank=True, null=True)
    description = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
