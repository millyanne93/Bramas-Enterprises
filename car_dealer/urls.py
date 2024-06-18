from django.urls import path
from . import views
from .views import index, CarDealerLoginView, logout_view

urlpatterns = [
        path('', views.index, name='index'),
        path('home/', views.home, name='home'),
        path('base/', views.base, name='base'),
        path('login/', CarDealerLoginView.as_view(), name='login'),
        path('logout/', views.logout_view, name='logout_view'),
        path('register/', views.register, name='register'),
        path('registration/', views.registration, name='registration'),
        path('add_car/', views.add_car, name='add_car'),
        path('manage_cars/', views.manage_cars, name='manage_cars'),
        path('booking_list/', views.view_booking_list, name='booking_list'), 
        path('complete_booking/<int:booking_id>/', views.complete_booking, name='complete_booking'),
        path('booking_history/', views.booking_history, name='booking_history'),
        path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
]
