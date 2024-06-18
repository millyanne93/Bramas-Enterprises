from django.contrib import admin
from .models import Location, CarDealer, Car

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'pincode', 'city')
    search_fields = ('name', 'address', 'pincode', 'city')

class CarDealerAdmin(admin.ModelAdmin):
    list_display = ('car_dealer', 'contact_info', 'location', 'wallet')
    search_fields = ('car_dealer__username', 'contact_info', 'location__name')

class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'capacity', 'price_per_day', 'available', 'location')
    search_fields = ('make', 'model', 'year', 'capacity', 'location__name')
    list_filter = ('available', 'year', 'location')

admin.site.register(Location, LocationAdmin)
admin.site.register(CarDealer, CarDealerAdmin)
admin.site.register(Car, CarAdmin)
# Register your models here.
