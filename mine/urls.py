from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard',views.livedash,name='livedash'),
    path('calculator',views.calculator,name='calculator'),
    path('CustomLogin/',views.customLogin,name='customLogin'),
    path('CustomLogout',views.customLogout,name='customLogout'),
    path('initiatives',views.initiatives,name='initiatives'),
    path('register/', views.register, name='register'),
         

]
