from django.db import models

# Create your models here.
class City(models.Model):
    cName = models.CharField(max_length = 20)
    exist = models.BooleanField()
    
    
class Hotel(models.Model):
    hName = models.CharField(max_length = 50)
    exist = models.BooleanField()
    
    hCity = models.ForeignKey(City)
    
class Room(models.Model):
    rPrice = models.IntegerField()
    rNum = models.CharField(max_length = 20)
    exist = models.BooleanField()
    
    roomFromHotel = models.ForeignKey(Hotel)

class Customer(models.Model):
    emailAdd = models.CharField(max_length = 30)
    fullName = models.CharField(max_length = 30)
    exist = models.BooleanField()
    
class Reserve(models.Model):
    checkInTime = models.DateTimeField()
    checkOutTime = models.DateTimeField()
    adultNum = models.IntegerField()
    minorNum = models.IntegerField()
    exist = models.BooleanField()
    
    reserver = models.ForeignKey(Customer)
    reserveRoom = models.ForeignKey(Room)
    
