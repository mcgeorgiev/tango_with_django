from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Constructs a dict to pass to the template as its context
    context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}

    # Returns a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # Constructs a dict to pass to the template as its context
    context_dict = {"title": "This is the about page", "name": "Michael"}
    
    # Returns a rendered response to send to the client
    return render(request, 'rango/about.html', context=context_dict)
