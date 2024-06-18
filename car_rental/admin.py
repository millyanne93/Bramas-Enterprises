from django.contrib import admin
from .models import Booking, UserProfile

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'car_dealer', 'rent', 'days')
    search_fields = ('user__username', 'car__make', 'car__model', 'car_dealer__car_dealer__username')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'location')
    search_fields = ('user__username', 'phone_number', 'address', 'location__name')

admin.site.register(Booking, BookingAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
