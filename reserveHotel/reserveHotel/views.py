from django.shortcuts import render
from django.core.context_processors import request

from reserveHotel.models import City, Hotel, Reserve, Room, User
# Create your views here.
def register(request):
    return render(request, 'reserveHotel/signup.html')

def log_in(request):
    return render(request, 'reserveHotel/signin.html')

def search_hotel(request):
    received_email = request.POST['email']
    received_pwd = request.POST['password']
    try:
        received_username = request.POST['uname']
    except:
        if(received_email == '' or received_pwd == ''):
            
            return render(request, 'reserveHotel/signin.html')
        else:
            try:
                p = User.objects.get(emailAdd = received_email)
            except:
                return render(request, 'reserveHotel/signin.html')
            else:
                if(p.password == received_pwd):
                    return render(request, 'reserveHotel/searchHotel.html')
                else:
                    return render(request, 'reserveHotel/signin.html')
    
    if(received_email == '' or received_username == '' or received_pwd == ''):
        return render(request, 'reserveHotel/signup.html')
    
    User.objects.create(emailAdd = received_email,
                        fullName = received_username,
                        password = received_pwd)

    return render(request, 'reserveHotel/searchHotel.html')

def search_result(request, city_id):
    city_id = City.objects.get(cName = request.POST['city']).id
    print city_id
    return render(request, 'reserveHotel/searchResult.html')

def choose_room(request):
    return render(request, 'reserveHotel/chooseRoom.html')

def room_confirm(request):
    return render(request, 'reserveHotel/roomConfirm.html')

def payment(request):
    return render(request, 'reserveHotel/payment.html')

def exception(request):
    return render(request, 'reserveHotel/exception.html')