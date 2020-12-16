from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Listing, Watchlist,Comment

from .models import User
from . import forms


def index(request):
    lists = Listing.objects.all()
    #image = lists.image()
    return render(request, "auctions/index.html", {
        "lists":lists
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = forms.CreateListing(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.listed_by = request.user
            instance.save()
            return redirect('index')
        else:
            return render(request,'auctions/create_listing.html',{
                "form":form
            })
                
    else:
        form = forms.CreateListing(request.POST)
        return render(request, 'auctions/create_listing.html',{
            "form":form
        })


def listing_details(request,list_id):
    if request.method =='POST':
        form = forms.Comment(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.commented_by = request.user
            instance.save()
            return HttpResponse("thank you for your comment!")
            
    else:
        form = forms.Comment(request.POST)
        listed = Listing.objects.get(pk = list_id)
        comments = Comment.objects.all()
        return render(request,'auctions/listing_details.html',{
            "list":listed,"form":form, "comments":comments
        })

def watchlist(request):
    if request.method == 'POST':
        form = forms.CreateWatchlist(request.POST)
        instance = form.save(commit=False)
        instance.save()
        return redirect('watchlist')
    else:
        return render(request,'auctions/watchlist.html')