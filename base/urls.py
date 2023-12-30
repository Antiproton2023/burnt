from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login',views.blogin,name='login'),
    path('signup',views.signup,name='signup'),
    path('',views.home,name='home'),
    path('logout',views.logoutpage,name='logout'),
    path('logoutsuccess',views.logoutSuccess,name = 'logoutsuccess'),
    path('createserver',views.createServer,name = 'createserver'),
    path('deleteServer/<str:password>',views.deleteServer,name='deleteServer'),
    path('ServerMainPage/<str:password>',views.ServerMainPage,name='ServerMainPage'),
    path('ManageMembers/<str:password>',views.ManageMembers,name='ManageMembers'),
    path('createroom/<str:password>',views.createroom,name = 'createroom'),
    path('room/<str:password>',views.room,name='room'),

]
