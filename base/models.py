from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
# Create your models here.


class UserExtra(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profilepicture = models.ImageField(upload_to='files/profilepics')
    FirstSignIn = models.BooleanField(default=True)


class Server(models.Model):
    name = models.CharField(max_length=50, unique=True)
    private = models.BooleanField(default = True)
    host = models.ForeignKey(User, on_delete= models.SET_NULL,null=True,unique = False)
    password = models.UUIDField(unique = True, default = uuid4)
    def __str__(self):
        return self.name
    
class member(models.Model):
    member = models.ForeignKey(User, on_delete = models.CASCADE,unique = False)
    server = models.ForeignKey(Server, on_delete = models.CASCADE,unique = False)

class Room(models.Model):
    name = models.CharField(max_length=50)
    server = models.ForeignKey(Server,on_delete=models.CASCADE)
    password = models.UUIDField(unique = True, default = uuid4)
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    msg = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    uniqueid = models.UUIDField(unique = True, default = uuid4)
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.msg[0:50]   


class Image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='files/imgs')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.img   