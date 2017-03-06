from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm

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
        # context_dict['pages'] = pages
        # context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

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


def about(request):
    return render(request, 'rango/about.html')