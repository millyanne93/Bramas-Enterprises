# car_rental/context_processors.py
from car_dealer.models import CarDealer

def user_type_context(request):
    context = {}
    if request.user.is_authenticated:
        try:
            CarDealer.objects.get(car_dealer=request.user)
            context['user_type'] = 'owner'
        except CarDealer.DoesNotExist:
            context['user_type'] = 'customer'
    return context
