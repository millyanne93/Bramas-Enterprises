from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#URLConf
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('confirmed/', views.confirm, name='confirmed'),
    path('confirmation/', views.rent_car, name='confirmation'),
    path('manage/', views.manage, name='manage'),
    path('update_order/', views.update_order, name='update_order'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('get_user_data/', views.get_user_data, name='get_user_data'),
    path('custom_logout/', views.CustomLogoutView.as_view(), name='custom_logout'),
]
