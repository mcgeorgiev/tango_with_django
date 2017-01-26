import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twd.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

    # pages we want to add to a category
    python_pages = [
        {
            "title": "Official Python Tutorial",
            "url":"http://docs.python.org/2/tutorial/",
            "views":10
        },
        {
            "title":"How to Think like a Computer Scientist",
            "url":"http://www.greenteapress.com/thinkpython/",
            "views":32
        },
        {
            "title":"Learn Python in 10 Minutes",
            "url":"http://www.korokithakis.net/tutorials/python/",
            "views":17
        }
    ]

    django_pages = [
        {
            "title":"Official Django Tutorial",
            "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
            "views":21
        },
        {
            "title":"Django Rocks",
            "url":"http://www.djangorocks.com/",
            "views":31
        },
        {
            "title":"How to Tango with Django",
            "url":"http://www.tangowithdjango.com/",
            "views":4
        }
    ]

    other_pages = [
        {
            "title":"Bottle",
            "url":"http://bottlepy.org/docs/dev/",
            "views":0
        },
        {
            "title":"Flask",
            "url":"http://flask.pocoo.org",
            "views":24
        }
    ]

    categories = {"Python": {"pages": python_pages, "likes": 64, "views": 128},
            "Django": {"pages": django_pages, "likes": 32, "views": 64},
            "Other Frameworks": {"pages": other_pages, "likes": 16, "views": 32}}



    for category, category_data in categories.iteritems():
        cat = add_category(category, category_data["likes"], category_data["views"])
        for pg in category_data["pages"]:
            add_page(cat, pg["title"], pg["url"], pg['views'])

    for cat in Category.objects.all():
        for pg in Page.objects.filter(category=cat):
            print "- {0} - {1}".format(str(cat), str(pg))

def add_page(cat, title, url, views):
    # get_or_create -> returns object, created(boolean)
    pg = Page.objects.get_or_create(category=cat, title=title)[0]
    pg.url=url
    pg.views=views
    pg.save()
    return pg

def add_category(name, likes, views):
    cat = Category.objects.get_or_create(name=name)[0]
    cat.likes=likes
    cat.views=views
    cat.save()
    return cat

if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
