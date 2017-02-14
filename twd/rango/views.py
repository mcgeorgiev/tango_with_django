from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

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


def add_category(request):
    form = CategoryForm()

    # if a HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            print cat, cat.slug
            # most recent added category is on index page so redirect
            return index(request)
        else:
            print form.errors

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print form.errors

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    print request
    # whether the registration is successful
    registered = False

    if request.method == 'POST':

        # get raw info from the forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # false = delays saving the model to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        # not a HTTP POST so we render a form blank, ready for input
        print 'Not a post'
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                    'rango/register.html',
                    {'user_form': user_form,
                     'profile_form': profile_form,
                     'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # None if not valid
        user = authenticate(username=username, password=password)

        if user:
            # could be disabled account
            if user.is_active:
                login(request, user)
                # 302 response = redirect
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled")
        else:
            # bad login details
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied")

    else:
        # not a post
        return render(request, 'rango/login.html', {})
