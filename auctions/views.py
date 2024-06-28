from .forms import listing # Importing Django form class
from .models import Auctionlistings # Importing model class from models.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User


def index(request):
    rows = Auctionlistings.objects.all()
    return render(request, "auctions/index.html", {
        'rows': rows,
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
            return redirect(index)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect(index)


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
        return redirect(index)
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login/") # Making sure the user is logged in
def create(request):
    if request.method == 'POST':
        form = listing(request.POST) # Getting the form data from the POST
        if form.is_valid():
            # Process the data with form.is_cleaned
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            # image_url = form.cleaned_data['image_url']
            category = form.cleaned_data['category']

            # Adding all the data in Auctionlistings model class
            auction_listing = Auctionlistings.objects.create(
                user = request.user,
                title = title,
                description =  description, 
                bid = bid,
                category = category,
                )

            return redirect(index)
    else:
        form = listing()
        return render(request, 'auctions/create.html', {
            'form': form
        })


def listings(request, listing_id):
    if request.method == 'POST':
        listing = Auctionlistings.objects.get(pk=listing_id) # Getting the listing, which should be added to the watchlist

        if request.POST['form_id'] == 'form2': # If the user clicked add watchlist button
            request.user.watchlist.add(listing) # Adding the listing into the user's watchlist
        elif request.POST['form_id'] == 'form1': # If the user clicked remove watchlist button
            request.user.watchlist.remove(listing) # Remove the listing from the user's watchlist

        return redirect(listings, listing_id=listing_id)

    else: # If the request is GET
        # Getting the Auctionlistings with id
        listing = Auctionlistings.objects.get(pk=listing_id)
        return render(request, 'auctions/listing.html', {
        'listing': listing,
        })