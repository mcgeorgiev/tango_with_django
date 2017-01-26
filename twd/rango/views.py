from django.shortcuts import render
from django.http import HttpResponse

# Import the Category model
from rango.models import Category

def index(request):
    # orders the categories by likes in "-" descending order, top 5
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {"categories": category_list}

    # Returns a rendered response to send to the client
    return render(request, 'rango/index.html', context_dict)


def about(request):
    # Constructs a dict to pass to the template as its context
    context_dict = {"title": "This is the about page", "name": "Michael"}

    # Returns a rendered response to send to the client
    return render(request, 'rango/about.html', context=context_dict)
