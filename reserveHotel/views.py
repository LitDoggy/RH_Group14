from django.shortcuts import render
from reserveHotel.models import City, Hotel, Reserve, Room, User

# Create your views here.
current_user = None
choosed_city = "NULL"
choosed_hotel = "NULL"
check_in_date = 1/1/1
check_out_date = 1/1/1
available_room = []

roomNum = 0
resident = []
totalPrice = 0

def register(request):
    return render(request, 'reserveHotel/signup.html')

def log_in(request):
    return render(request, 'reserveHotel/signin.html')

def search_hotel(request):
    global current_user
    if(current_user != None):
        return render(request, 'reserveHotel/searchHotel.html')
    
    received_email = request.POST['email']
    received_pwd = request.POST['password']
    try:
        received_name = request.POST['uname']
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
                    current_user = User.objects.get(emailAdd = received_email)
                    return render(request, 'reserveHotel/searchHotel.html')
                else:
                    return render(request, 'reserveHotel/signin.html',
                                  {'error_message': 'Incorrect password'})
    
    if(received_email == '' or received_name == '' or received_pwd == ''):
        return render(request, 'reserveHotel/signup.html',
                      {'error_message': 'Sign up information not completed!'})
    
    current_user = User(emailAdd = received_email,
                        fullName = received_name,
                        password = received_pwd)
    current_user.save()

    return render(request, 'reserveHotel/searchHotel.html')

def search_result(request):
    global choosed_city, available_room, check_in_date, check_out_date
    choosed_city = request.POST['city']

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
    available_room = siftRoom(check_in_date, check_out_date, roomList)
    print available_room
    print 'available_room'
    availableHotelList = judgeHotelFromRoom(available_room)

    return render(request, 'reserveHotel/searchResult.html', 
                            {'city_name': choosed_city, 
                             'checkout_date': check_out_date, 
                             'checkin_date': check_in_date,
                             'availableHotels': availableHotelList,}
                  )

def choose_room(request):
    global choosed_hotel
    choosed_hotel = request.POST['hotel_name']
    print choosed_hotel
    print choosed_city
    return render(request, 'reserveHotel/chooseRoom.html',
                  {'hotel_name': choosed_hotel,
                   'city_name': choosed_city})

def room_confirm(request):
    global roomNum,totalPrice
    roomNum = request.POST['count']
    
    if(int(roomNum) > len(available_room)):
        return render(request, 'reserveHotel/chooseRoom.html',
                      {'error_message': 'Sorry! We have no enough room!',
                       'hotel_name': choosed_hotel,
                       'city_name': choosed_city})
        
    print roomNum

    for i in range(1, int(roomNum) + 1):        
        postMsg = 'room' + str(i) + '_adults'
        adultsNum = request.POST[postMsg]
        postMsg = 'room' + str(i) + '_children'
        childrenNum = request.POST[postMsg]
        resident.append([adultsNum, childrenNum])
        #i += 1
        print i, roomNum
    
    print resident
    print available_room
    roomList = available_room[0 : int(roomNum)]
    print roomList

    for room in roomList:
        totalPrice += room.rPrice
    print totalPrice
    
    return render(request, 'reserveHotel/roomConfirm.html',
                  {'city_name': choosed_city,
                   'hotel_name': choosed_hotel,
                   'checkin_date': check_in_date,
                   'checkout_date': check_out_date,
                   'room_num': roomNum,
                   'room_list': available_room[0 : int(roomNum)],
                   'total_price': totalPrice,})

def payment(request):
    global check_in_date, check_out_date
    reserverName = request.POST['full_name']
    reserverEmail = request.POST['email']
    if(reserverName == "" or reserverEmail == ""):
        return render(request, 'reserveHotel/roomConfirm.html',
                      {'error_message': 'You didn\'t complete personal information!',
                       'city_name': choosed_city,
                       'hotel_name': choosed_hotel,
                       'checkin_date': check_in_date,
                       'checkout_date': check_out_date,
                       'room_num': roomNum,
                       'room_list': available_room[0 : int(roomNum)],
                       'total_price': totalPrice,})
        
    
    a = check_in_date.split('/')
    a.reverse()
    temp = a[2]
    a[2] = a[1]
    a[1] = temp
    
    check_in_date = a[0] + '-' + a[1] + '-' + a[2]
    
    a = check_out_date.split('/')
    a.reverse()
    temp = a[2]
    a[2] = a[1]
    a[1] = temp
    
    check_out_date = a[0] + '-' + a[1] + '-' + a[2]
    
    print check_in_date
     
    for i in range(1, int(roomNum) + 1):
        Reserve.objects.create(checkInTime = check_in_date, checkOutTime = check_out_date,
                               adultNum = resident[i - 1][0], minorNum = resident[i - 1][1],
                               representive = reserverName, repreMail = reserverEmail,
                               reserver = current_user, exist = 1,
                               reserveRoom = available_room[i - 1])
        
    return render(request, 'reserveHotel/payment.html',
                  {'room_list': available_room[0 : int(roomNum)],
                   'total_price': totalPrice,})

def over(request):
    global totalPrice
    reserveRoom = []
    for i in range(1, int(roomNum) + 1):
        reserveRoom.append(available_room[i - 1])
    
    print reserveRoom
    totalPrice = 0
    return render(request, 'reserveHotel/over.html', 
                  {})

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
            checkIn = ei.split('/')
            checkOut = eo.split('/')
            print record.reserveRoom
            print ' checkTime'
            if((dateJudge(record.checkInTime, checkIn) >= 0 and dateJudge(record.checkInTime, checkOut) < 0)
                or (dateJudge(record.checkOutTime, checkIn) > 0 and dateJudge(record.checkOutTime, checkOut) <= 0)):
                print record.reserveRoom
                print ' timeNotCapable'
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
    
def dateJudge(former, latter):
    print former, latter
    print former.year, former.month, former.day
    print latter[0], latter[1], latter[2]
    
    if(former.year < int(latter[2])):
        return -1
    elif(former.year > int(latter[2])):
        return 1
    else:
        if(former.month < int(latter[0])):
            return -1
        elif(former.month > int(latter[0])):
            return 1
        else:
            if(former.day < int(latter[1])):
                return -1
            elif(former.day > int(latter[1])):
                return 1
            else:
                print 'equals'
                return 0
            