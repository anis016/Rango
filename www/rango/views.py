from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Rango Says ... Hey there partner ! <br> <a href='about'>About</a>")

def about(request):
    return HttpResponse("About page! <br> <a href='index'>Main</a>")