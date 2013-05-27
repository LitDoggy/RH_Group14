import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lab2.settings")

from reserveHotel.models import User, City, Hotel, Room

u = User(emailAdd = 'abc', fullName = 'yoh', password = 'pwd', exist = 1)
u.save()

User.objects.create(emailAdd = 'mail', exist = 1, 
					fullName = 'toe', password = 'monkey')
User.objects.create(emailAdd = 'lab2', exist = 1, 
					fullName = 'maria', password = '12345')

c = City(cName = 'New York', exist = 1)
c.save()
City.objects.create(cName = 'Caton', exist = 1)
City.objects.create(cName = 'London', exist = 1)

h = c.hotel_set.create(hName = 'Jan', exist = 1)
c.hotel_set.create(hName = 'Feb', exist = 1) 
c.hotel_set.create(hName = 'Mar', exist = 1)
c.hotel_set.create(hName = 'Apr', exist = 1) 

r = h.room_set.create(rPrice = '200', rNum = 'Mon', exist = 1)
h.room_set.create(rPrice = '230', rNum = 'Tue', exist = 1)
h.room_set.create(rPrice = '240', rNum = 'Wed', exist = 1)
