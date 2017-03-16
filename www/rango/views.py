from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from rango.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from rango.api.webhose import run_query
from django.shortcuts import redirect

# Create your views here.

def index(request):
    # request.session.set_test_cookie()

    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list}
    context_dict['pages'] = pages_list

    #### Below code works with checking COOKIE in client side ####
    # Obtain response object early so we can add cookie information
    # response = render(request, 'rango/index.html', context=context_dict)
    # call the helper function to handle the cookies
    #visitor_cookie_handler(request, response)
    ##############################################################

    ### Below code works with checking COOKIE in client side ####
    # No need to obtain response object early as we are getting the data from server side
    # call the helper function to handle the cookies
    visitor_cookie_handler_using_session(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    #############################################################

    return response

def visitor_cookie_handler(request, response):
    # Get the number of visits to the site
    # We use the COOKIES.get() function to obtain the visits cookie
    visits = int(request.COOKIES.get('visits', '1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time   = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 2:
        visits += 1
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        visits = 1
        response.set_cookie('last_visit', last_visit_cookie)

    response.set_cookie('visits', visits)


def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler_using_session(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def webhose_search(request):
    result_list = []
    query = ""
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})

def show_category(request, category_name_slug):
    context_dict = {}
    try :
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict = {'pages': pages, 'category': category}
        # print("context_dict: ", context_dict)
        # context_dict['pages'] = pages
        # context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    ### Merging Webhose search with Category
    context_dict['query'] = category.name
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list

    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'GET':
        pass
        # print(request.method + " method automatically called")

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

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)  # load the category after/before submitting form
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        page_form = PageForm(request.POST)  # binding data from the POST request to the form
        # print("form: ", form)
        if page_form.is_valid(): # We call the form’s is_valid() method;
                            # if it’s not True, we go back to the template with the form.
            if category:
                page = page_form.save(commit=False)
                page.category = category
                page.views = 0
                page.save() # do the save now, once category is inserted
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    # if method is GET request
    # print("category_name_slug", category_name_slug)
    page_form = PageForm() ## If method is GET request, it will create the PageForm

    # perform when submitting the form or POST request

    context_dict = {'form': page_form, 'category': category} ## load the form
    return render(request, 'rango/add_page.html', context_dict)

# def register(request):
#     # A boolean value to tell whether the registration was successful.
#     registered = False # By default, registration is not successful
#
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         userprofile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and userprofile_form.is_valid():
#             # save the user's form data to the database.
#             # Direct save is possible as it already has password data from form
#             user = user_form.save()
#
#             # hash the provided password using set_password() method
#             user.set_password(user.password)
#
#             # update the user in the database with hashed password
#             user.save()
#
#             ## Now sortout the user_profile form
#             # We can't directly save the userprofile as we need to provide the user instance else it will
#             # violate the integrity
#             profile = userprofile_form.save(commit=False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             # Now we can save the userprofile
#             profile.save()
#
#             # Everything done ! Thus change the value of registered to True
#             registered = True
#         else:
#             # print the errors in the Console
#             print(user_form.errors, userprofile_form.errors)
#     else:
#         # Load both the forms for the request.GET method
#         user_form = UserForm()
#         userprofile_form = UserProfileForm()
#
#     context_dict = {'user_form': user_form, 'profile_form': userprofile_form, 'registered': registered}
#     # Render the template depending upon the context
#     return render(request, 'rango/register.html', context=context_dict)

# def user_login(request):
#     # If request.method == 'POST', try to pull out the relevant information
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password) # django's own matchin mechanism
#         if user:
#             if user.is_active:
#                 login(request, user) ## django login method
#                 print("Login success !")
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse("Your Account is disabled.")
#         else:
#             print("Invalid login details: {0} {1}".format(username, password))
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         # load the login form for the GET request
#         return render(request, 'rango/login.html')

# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))

def about(request):
    # if request.session.test_cookie_worked():
    #     print("TEST COOKiE WORKED !")
    #     request.session.delete_test_cookie()

    return render(request, 'rango/about.html')


class MyRegistrationView(RegistrationView):
    print("coming here or not !")
    def get_success_url(self, user=None):
        print("hitting get_succss_url")
        return reverse('rango:register_profile')


def track_url(request):
    page_id = None
    url = '/rango/'

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                print("There is some issue in try block ! debug it out ...")

    return redirect(url)

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'rango/profile_registration.html', context_dict)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
    print(userprofile.picture)

    return render(request, 'rango/profile.html', {'form': form, 'userprofile': userprofile, 'selecteduser': user})

def list_profiles(request):
    try:
        userprofile_list = UserProfile.objects.all()
    except UserProfile.DoesNotExist:
        return redirect('index')

    return render(request, 'rango/list_profiles.html', {'userprofile_list': userprofile_list})