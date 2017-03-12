from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

# Create your views here.

def index(request):
    category_list = Category.objects.order_by('-likes')[:10]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list}
    context_dict['pages'] = pages_list
    return render(request, 'rango/index.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try :
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict = {'pages': pages, 'category': category}
        print("context_dict: ", context_dict)
        # context_dict['pages'] = pages
        # context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'GET':
        print(request.method + " method automatically called")

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # check for validation on the data
        if form.is_valid():
            form.save(commit=True)
            return index(request) # redirecting to the index page(index function)
        else:
            # as of now print the error in the terminal
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)  # load the category after/before submitting form
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        form = PageForm(request.POST)  # binding data from the POST request to the form
        # print("form: ", form)
        if form.is_valid(): # We call the form’s is_valid() method;
                            # if it’s not True, we go back to the template with the form.
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save() # do the save now, once category is inserted
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    # if method is GET request
    # print("category_name_slug", category_name_slug)
    form = PageForm() ## If method is GET request, it will create the PageForm

    # perform when submitting the form or POST request

    context_dict = {'form': form, 'category': category} ## load the form
    return render(request, 'rango/add_page.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')