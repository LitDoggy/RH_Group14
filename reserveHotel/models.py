from django.db import models

# Create your models here.
class City(models.Model):
    cName = models.CharField(max_length = 20)
    exist = models.BooleanField()
    
    def __unicode__(self):
        return self.cName
    
class Hotel(models.Model):
    hName = models.CharField(max_length = 50)
    exist = models.BooleanField()
    
    hCity = models.ForeignKey(City)
    
    def __unicode__(self):
        return self.hName
    
class Room(models.Model):
    rPrice = models.IntegerField()
    rNum = models.CharField(max_length = 20)
    exist = models.BooleanField()
    
    roomFromHotel = models.ForeignKey(Hotel)
    
    def __unicode__(self):
        return self.rNum

class User(models.Model):
    emailAdd = models.CharField(max_length = 30)
    fullName = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    
    exist = models.BooleanField()
    
    def __unicode__(self):
        return self.fullName
    
class Reserve(models.Model):
    checkInTime = models.DateTimeField()
    checkOutTime = models.DateTimeField()
    adultNum = models.IntegerField()
    minorNum = models.IntegerField()
    representive = models.CharField(max_length = 50)
    repreMail = models.CharField(max_length = 100)
    
    exist = models.BooleanField()
    
    reserver = models.ForeignKey(User)
    reserveRoom = models.ForeignKey(Room)
    
    def __unicode__(self):
        return self.reserver
