from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from . import models
import time
# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username = form.cleaned_data['username'])
            login(request,user)
            return redirect('home')
    context = {'form':form}
    return render(request,'signup.html',context)

def blogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except:
                messages.error(request,"User does not exist.")
        authUser = authenticate(request,username=username,password=password)
        if authUser is not None:
            login(request,authUser)
            return redirect('home')
        else:
            messages.error(request,'Wrong Password')


    context = {}
    return render(request,"login.html",context)

@login_required(login_url="login")
def home(request):
    try:
        members = models.member.objects.filter(member = request.user)

    except:
        pass
    context = {'partof':members}
    return render(request,"home.html",context)
@login_required(login_url='login')
def logoutpage(request):
    logout(request)
    return redirect('logoutsuccess')

def logoutSuccess(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'logoutsuccess.html')
@login_required(login_url='login')
def createServer(request):
    if request.method == 'POST':
        serverName = request.POST.get('servername')
        serverHost = request.user
        try:
            s = models.Server.objects.get(name= serverName)
            if s:
                messages.error(request,'Server with a similar name aldready exists.')
        except:
            server = models.Server.objects.create(name = serverName,host = serverHost)
            m1 = models.member.objects.create(member = serverHost,server=server)
            return redirect('home')
    return render(request,'createserver.html')
@login_required(login_url='login')
def deleteServer(request,password):
    servertoDelete = models.Server.objects.get(password=password)
    if request.method == 'POST':
        servertoDelete.delete()
        return redirect('home')    
    context = {'s':servertoDelete}    
    return render(request,'deleteServer.html',context)

@login_required(login_url='login')
def ServerMainPage(request,password):
    server = models.Server.objects.get(password=password)
    members = models.member.objects.filter(server=server)
    myrooms = models.Room.objects.filter(server = server)
    context = {'s':server,'members':members,'rooms':myrooms}
    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        room = models.Room.objects.get(name = roomname,server=server)
        room.delete()
    return render(request,'ServerMainPage.html',context)

@login_required(login_url='login')
def ManageMembers(request,password):
    users = models.User.objects.all()
    server = models.Server.objects.get(password=password)
    if request.user != server.host: return redirect('request.META.HTTP_REFERER')
    if request.method == 'GET':
        name = request.GET.get('SearchUser')    
        if not name : name = ''
        users = models.User.objects.filter(username__icontains = name)
    
    if request.method == 'POST' and request.POST.get('myaction')=='add':
        username = request.POST.get('username')
        toadd = models.User.objects.get(username=username)
        try:
            m = models.member.objects.get(member=toadd, server = server);
        except:
            m = models.member.objects.create(member=toadd, server = server);  
    if request.method == 'POST' and request.POST.get('myaction')=='remove':
        username = request.POST.get('username')
        toremove = models.User.objects.get(username=username)      
        m = models.member.objects.get(member=toremove, server = server)
        m.delete()
    members = models.member.objects.filter(server=server)
    context = {'s':server,'members':members,'users':users}
    return render(request,'ManageMembers.html',context)

@login_required(login_url='login')
def createroom(request,password):
    server = models.Server.objects.get(password=password)
    users = models.User.objects.all()
    members = models.member.objects.filter(server=server)
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            room = models.Room.objects.get(name = name, server = server)  
            messages.error(request, 'Room aldready exists')
        except:
            room = models.Room.objects.create(name = name, server = server) 
            return redirect('home')
    context = {'s':server,'members':members,'users':users}
    return render(request,'createroom.html',context)

@login_required(login_url='login')
def room(request,password):
    if request.method == 'POST':
        if request.POST.get('myaction') == 'admsg':
            msg = request.POST.get('msg')
            user = request.user
            room = models.Room.objects.get(password=password)
            testmsg = 0
            for letter in msg:
                if letter != ' ':
                    testmsg+=1
            if testmsg !=0:
                mymsg = models.Message.objects.create(msg = msg, room = room, user = user)
                return redirect('room',password = room.password)
    if request.method == 'POST':
        if request.POST.get('myaction') == 'dmsg':
            msg = request.POST.get('msgbody')
            user = request.user
            room = models.Room.objects.get(password=password)
            uniqueid = request.POST.get('uniqueid')
            mymsg = models.Message.objects.get(msg=msg,uniqueid=uniqueid,user=user,room=room)
            mymsg.delete()
            return redirect('room',password = room.password)
    room = models.Room.objects.get(password=password)
    mymessages = models.Message.objects.filter(room = room)
    context = {'room':room, 'mymessages':mymessages}
    return render(request,'room.html',context)