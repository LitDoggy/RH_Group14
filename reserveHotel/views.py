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
            
            return render(request, 'reserveHotel/signin.html', 
                          {'error_message': "Sign in information not completed!"})
        else:
            try:
                p = User.objects.get(emailAdd = received_email)
            except:
                return render(request, 'reserveHotel/signin.html',
                              {'error_message': "Incorrect email!"})
            else:
                if(p.password == received_pwd):
                    return render(request, 'reserveHotel/searchHotel.html')
                else:
                    return render(request, 'reserveHotel/signin.html',
                                  {'error_message': 'Incorrect password'})
    
    if(received_email == '' or received_username == '' or received_pwd == ''):
        return render(request, 'reserveHotel/signup.html',
                      {'error_message': 'Sign up information not completed!'})
    
    User.objects.create(emailAdd = received_email,
                        fullName = received_username,
                        password = received_pwd)

    return render(request, 'reserveHotel/searchHotel.html')

def search_result(request):
    city_name = request.POST['city']

    #print city_name
    checkin_date = request.POST['checkin']
    checkout_date = request.POST['checkout']
    if(checkin_date == "" or checkout_date == "" or city_name == ""):
        return render(request, 'reserveHotel/searchHotel.html', 
                      {'error_message': "Information not completed"})
    try:
        city = City.objects.get(cName = city_name).id
    except:
        errorMsg = 'City \'' + city_name + '\' Does Not Exist!'
        return render(request, 'reserveHotel/searchHotel.html',
                      {'error_message': errorMsg})
        
    hotelList = Hotel.objects.filter(hCity = city)
    print hotelList
    roomList = getRoomFromHotel(hotelList)
    availableRoomList = siftRoom(checkin_date, checkout_date, roomList)
    availableHotelList = judgeHotelFromRoom(availableRoomList)
    print availableHotelList
    
    return render(request, 'reserveHotel/searchResult.html', 
                            {'city_name': city_name, 
                             'checkout_date': checkout_date, 
                             'checkin_date': checkin_date,
                             'availableHotels': availableHotelList,}
                  )

def choose_room(request):
    return render(request, 'reserveHotel/chooseRoom.html')

def room_confirm(request):
    return render(request, 'reserveHotel/roomConfirm.html')

def payment(request):
    return render(request, 'reserveHotel/payment.html')

def exception(request):
    return render(request, 'reserveHotel/exception.html')

def getRoomFromHotel(allHotel):
    roomList = []
    for hotel in allHotel:
        for room in Room.objects.all():
            if(room.roomFromHotel == hotel):
                roomList.append(room)
    
    print roomList
    return roomList

def siftRoom(ei, eo, allRoom):
    #siftedRoomList = []
    allRecord = Reserve.objects.all()
    
    for record in allRecord:
        if(record.reserveRoom in allRoom):
            if((record.checkInTime >= ei and record.checkInTime < eo)
                or (record.checkOutTime > ei and record.checkOutTime <= eo)):
                allRoom.remove(record.reserveRoom)
    
    print allRoom
    return allRoom

def judgeHotelFromRoom(availableRoom):
    availableHotel = []
    print availableRoom
    for room in availableRoom:
        print room
        if(room.roomFromHotel not in availableHotel):
            availableHotel.append(room.roomFromHotel)
    print availableHotel
    return availableHotel
    
