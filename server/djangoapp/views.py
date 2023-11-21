from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context["message"] = "Invalid Username or Password"
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['password']
        user_exists = False
        try:
            User.objects.get(username=username)
            user_exists = True
        except:
            logger.debug("{} is successfully registered".format(username))
        if not user_exists:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == 'GET':
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/381222d1-3fc7-4759-9f8f-3a6a72715c3b/api/dealerships"
        try:
            dealerships = get_dealers_from_cf(url)
            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
            return HttpResponse(dealer_names)
        except Exception as e:
            context["message"] = f"Failure loading dealerships: {str(e)}"
            return render(request, 'djangoapp/index.html', context)



# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/381222d1-3fc7-4759-9f8f-3a6a72715c3b/api/review"
        try:
            reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
            dealer_reviews = ' '.join([review.review for review in reviews])
            return HttpResponse(dealer_reviews)
        except Exception as e:
            context["message"] = f"Failure loading reviews: {str(e)}"
            return render(request, 'djangoapp/index.html', context)



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

