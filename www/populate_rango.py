import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'www_site.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/",
         "views": 234657},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython",
         "views": 45454},
        {"title": "Learn Python in 10 minutes",
         "url": "http://www.korokithakis.net/tutorials/python",
         "views": 12347},
    ]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": 780},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": 500},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views": 450}
    ]

    character_pages = [
        {"title": "Himu",
         "url": "www.himu.com",
         "views": 19},

        {"title": "Masud Rana",
         "url": "www.masudrana.com",
         "views": 100},

        {"title": "Kishor Pasha",
         "url": "www.pasha.com",
         "views": 5502},
    ]

    novel_pages = [
        {"title": "Tin Goyenda",
         "url": "www.tingoyenda.com",
         "views": 12338},

        {"title": "Sherlock Holmes",
         "url": "www.sherlock.com",
         "views": 2313},
    ]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/",
         "views": 780},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": 800}
    ]

    ## Category name should be unique
    categories = {
        "Python": {"pages": python_pages, "views": 128, "likes": 64},
        "Django": {"pages": django_pages, "views": 64, "likes": 32},
        "Other Frameworks": {"pages": other_pages, "views": 80000, "likes": 12036},
        "Character": {"pages": character_pages, "views": 100, "likes": 48},  ## name: unique
        "Novel": {"pages": novel_pages, "views": 528, "likes": 164}
    }

    for category, category_data in categories.items():
        # print("{} - views: {}, likes: {} ".format(category, category_data.get("views", 0), category_data.get("likes", 0)))
        c = add_category(category, category_data.get("views", 0), category_data.get("likes", 0))
        for p in category_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_category(name, views = 0, likes = 0):
    ## https://docs.djangoproject.com/en/1.10/ref/models/querysets/#get-or-create
    # Returns a tuple of (object, created), where object is the retrieved or created object and
    # created is a boolean specifying whether a new object was created.
    # we are interested only with the object part, hence used [0] to get the 1st part(object)
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

def add_page(category, title, url, views = 0):
    p = Page.objects.get_or_create(category=category, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()