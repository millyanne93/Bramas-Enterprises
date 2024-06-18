from django import forms
from .models import CarDealer
from .models import Car

class CarDealerForm(forms.ModelForm):
    class Meta:
        model = CarDealer
        fields = ['contact_info', 'location', 'wallet', 'mobile']
        # You can exclude 'car_dealer' field as it is auto-generated from the OneToOneField with User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            # Add any additional customization if needed
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'capacity', 'price_per_day', 'photo', 'description']
