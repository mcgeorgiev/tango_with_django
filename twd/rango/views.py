from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Page

# Import the Category model
from rango.models import Category

def index(request):
    # orders the categories by likes in "-" descending order, top 5
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {"categories": category_list, "pages": page_list}

    # Returns a rendered response to send to the client
    return render(request, 'rango/index.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # try to find a category name slug with a given name, raise exception otherwise
        category = Category.objects.get(slug=category_name_slug)

        # retrieve all the associated pages
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Template will display the no category message for us
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


def about(request):
    # Constructs a dict to pass to the template as its context
    context_dict = {"title": "Rango says here is the about page.", "name": "Michael"}

    # Returns a rendered response to send to the client
    return render(request, 'rango/about.html', context=context_dict)
