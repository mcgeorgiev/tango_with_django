from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Hello World!</h1><br/>Please click <a href='/rango/about'>here</a> to view the about page")

def about(request):
    return HttpResponse("<h1>About</h1><br/>This is the about page.</br><a href='/rango/'>Back</a>")
