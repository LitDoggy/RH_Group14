from django.shortcuts import render
from django.core.context_processors import request
# Create your views here.
def register(request):
    return render(request, 'reserveHotel/signup.html')

def log_in(request):
    return render(request, 'reserveHotel/signin.html')

def search_hotel(request):
    return render(request, 'reserveHotel/searchHotel.html')

def search_result(request):
    return render(request, 'reserveHotel/searchResult.html')

def choose_room(request):
    return render(request, 'reserveHotel/chooseRoom.html')

def room_confirm(request):
    return render(request, 'reserveHotel/roomConfirm.html')

def payment(request):
    return render(request, 'reserveHotel/payment.html')