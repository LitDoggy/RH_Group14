from django.shortcuts import render
from django.core.context_processors import request

from reserveHotel.models import City, Hotel, Reserve, Room, User
# Create your views here.
choosed_city = "NULL"
check_in_date = 1/1/1
check_out_date = 1/1/1

roomNum = 0

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
    global choosed_city
    choosed_city = request.POST['city']

    #print city_name
    check_in_date = request.POST['checkin']
    check_out_date = request.POST['checkout']
    if(check_in_date == "" or check_out_date == "" or choosed_city == ""):
        return render(request, 'reserveHotel/searchHotel.html', 
                      {'error_message': "Information not completed"})
    try:
        city = City.objects.get(cName = choosed_city).id
    except:
        errorMsg = 'City \'' + choosed_city + '\' Does Not Exist!'
        return render(request, 'reserveHotel/searchHotel.html',
                      {'error_message': errorMsg})
        
    hotelList = Hotel.objects.filter(hCity = city)
    print hotelList
    roomList = getRoomFromHotel(hotelList)
    availableRoomList = siftRoom(check_in_date, check_out_date, roomList)
    availableHotelList = judgeHotelFromRoom(availableRoomList)
    print availableHotelList
    
    return render(request, 'reserveHotel/searchResult.html', 
                            {'city_name': choosed_city, 
                             'checkout_date': check_out_date, 
                             'checkin_date': check_in_date,
                             'availableHotels': availableHotelList,}
                  )

def choose_room(request):
    choosed_hotel = request.POST['hotel_name']
    print choosed_hotel
    print choosed_city
    return render(request, 'reserveHotel/chooseRoom.html',
                  {'hotel_name': choosed_hotel,
                   'city_name': choosed_city})

def room_confirm(request):
    count = request.POST['count']
    adults = request.POST['room1_adults']
    children = request.POST['room1_children']
    print adults
    print children
    print count
    return render(request, 'reserveHotel/roomConfirm.html')

def payment(request):
    roomCount = request.POST['count']
    
    return render(request, 'reserveHotel/payment.html')

def over(request):
    return render(request, 'reserveHotel/over.html')

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
    