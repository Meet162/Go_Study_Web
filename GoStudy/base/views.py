from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# rooms = [
# # list and dict
#     {'id': 1, 'name': 'Learn the Python' },
#     {'id': 2, 'name': 'Design Front-End'},
#     {'id': 3, 'name': 'Design Back-End'},
#     # dict  
#     ]

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
 #5:  after the authentication it return the home

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
 #1: it's a sending method to the system to 1.) enter the data and verify it to step 2:
        try:
            user = User.objects.get(username=username )

 #2:           # verify that username is same as db if not then except, it only verify the username, that user have or not
        except:
            messages.error(request,'User Does Not Exist')
            # if except then return the message

        user  = authenticate(request, username=username, password=password)   
 #3:            # it verify that the username & password is same as a database or note

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'Username or Password does not exist')
 #4:

    context = {'page':page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    # context = {}
    return redirect('home')

# it direct logout the user

def registerPage(request):
    # page = 'register'
    form = UserCreationForm()
    # predefined form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

            # upper case == to loercase


    return render(request, 'base/login_register.html', {'form':form})
# it represent the register page    (processing)----------------------

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) &
        Q(name__icontains=q) |
        Q(description__icontains=q) ) 
    
    # serachbar topic name
    
    topics = Topic.objects.all()
#1: for model where topics == topic

    room_count = rooms.count()
#2: define the count of the room that available

    # for searchbar
#3: define the all methods that describe in the return by a var 'context'
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i

    room = Room.objects.get(id=pk)
#4: define the room model for room prop

    context = {'room': room}
    return render(request, 'base/room.html', context)

# it is called function based url
# create a function home when url request come from the web , 
# it come from the main url, and then to the app.url , and then the views , 

#The decorator of the login {if user is not recognized then can't access this fun, first login}
@login_required(login_url='login')
# this decorator a user that is not autho  they wil be redirect, first login and allow to access below prop

def createRoom(request):
#1: for createRoom function

    # define the form page (processing)------------------------
    form = RoomForm()

#2: sending the request for creating the room
    if request.method == 'POST':
        form = RoomForm(request.POST)
#3. specified for the model only

        if form.is_valid():
            form.save()
#4. if form is valid then save the form and redirect

        return redirect('home') 
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# without login can't access this prop, with only the decorator the first define the decorator access if satisfied then the def func is accessible

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) #for model object
# the room model have 4 columns in the table,so 'get' the called the all column by the use of 'id=pk'
    form = RoomForm(instance=room) # for form file that convert the model to room , it combine forward to the form to model to room, so now form is the room
    # the room and form has the two object for the model:db that is use to fetch the data from the model
#  the pk is the id of the url that define the different url for the base.urls.py
# that path follow as a : home/room/1, home/room/2. 

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
# first you need to login the site & then you are allowed to delete the room(without auth it can't allowed)
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here!!')

    if request.method == 'POST':
        room.delete()
#. room.delet() is a method that delete the room

        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

# def searchbar(request):
#     search_bar = {}
#     return render(request, 'base/searchbar.html', search_bar)

