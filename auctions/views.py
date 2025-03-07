from .forms import listing, bidform # Importing Django form class
from .models import Auctionlistings, Bids, Comments # Importing model class from models.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User

CATEGORY_CHOICES = {
    'ELEC': 'Electronics',
    'FASH': 'Fashion',
    'HOME': 'Home & Garden',
    'SPORT': 'Sports & Outdoors',
    'AUTO': 'Automotive',
    'TOYS': 'Toys & Hobbies',
    'HEAL': 'Health & Beauty',
    'COLL': 'Collectibles & Art',
    'BOOK': 'Books, Movies & Music',
    'BUSI': 'Business & Industrial',
    'PETS': 'Pet Supplies',
    'BABY': 'Baby Essentials',
}

def index(request):
    listings = Auctionlistings.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings,
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
        
    listing = Auctionlistings.objects.get(pk=listing_id) # Getting the Auctionlistings with id

    comments = Comments.objects.filter(listing=listing)

    form = bidform() # Bid form

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'bid_form': form,
        'comments': comments,
    })


def add_to_watchlist(request, listing_id):
    if request.method == 'POST':
        listing = Auctionlistings.objects.get(pk=listing_id) # Getting the listing, which should be added to the watchlist

        if request.POST['form_id'] == 'form1': # If the user clicked add watchlist button
            request.user.watchlist.add(listing) # Adding the listing into the user's watchlist
        if request.POST['form_id'] == 'form2': # If the user clicked remove watchlist button
            request.user.watchlist.remove(listing) # Remove the listing from the user's watchlist

        return redirect(listings, listing_id=listing_id)
    
    else:
        return HttpResponse('Not Allowed')
    

def bidfn(request, listing_id):
    if request.method == 'POST':

        listing = Auctionlistings.objects.get(pk=listing_id) # Getting the Auctionlistings with id

        form = bidform(request.POST) # Getting the bid form data from request

        if form.is_valid():
            # Process the data with form.is_cleaned
            bid_amount = form.cleaned_data['bid']

            # Check if the bid is bigger than the last bid, if not present an error
            if bid_amount > listing.bid:
                # Add bid to the Bids table
                Bids.objects.create(user=request.user, listing=listing, bid=bid_amount)

                # Update the Auctionlistings bid
                listing.bid = bid_amount
                listing.save()
            else:
                return render(request, 'auctions/listing.html', {
                    'listing': listing,
                    'bid_form': bidform(),
                    'message': 'The bid needs to be bigger than the last bid',
                })

        return redirect(listings, listing_id=listing_id)

    else:
        return HttpResponse('Not Allowed')
    

def close(request, listing_id):
    if request.method == 'POST':
        listing = Auctionlistings.objects.get(pk=listing_id)
        all_bids = listing.listing_bids.all()
        # if there were bids for this listing
        if all_bids:
            # It finds the max bid value by taking bid value as the key for the max fn
            max_obj = max(all_bids, key=lambda obj: obj.bid) 
            # User who won the auction
            won_user = max_obj.user 

            # Putting the user in the Auctionlistings winner field
            listing.winner = won_user
        
        # If the listing doesn't have any bids
        else: 
            # Update the listings active status
            listing.active = False
                        
        # Save
        listing.save()

        return redirect(listings, listing_id=listing.id)

    else:
        return HttpResponse('Not Allowed')
    

def comment(request, listing_id):
    if request.method == 'POST':
        listing = Auctionlistings.objects.get(pk=listing_id)
        comment = request.POST['comment']

        # Add a Comment object
        Comments.objects.create(user=request.user, listing=listing, comments=comment)

        # Redirect to listing page
        return redirect(listings, listing_id=listing_id)

    else:
        return HttpResponse('Not Allowed')
    

@login_required(login_url="/login/") # Making sure the user is logged in
def watchlist(request):

    # Getting all the listings in the watchlist of the logged in user
    listings = request.user.watchlist.all()

    return render(request, 'auctions/watchlist.html', {
        'listings': listings,
    })


def categories(request):
    return render(request, 'auctions/categories.html', {
        'CATEGORY_CHOICES': CATEGORY_CHOICES,
    })


def categories_key(request, key):

    # It gets all the listings of the particular category
    listings = Auctionlistings.objects.filter(category=key)

    return render(request, 'auctions/categories.html', {
        'listings': listings,
    })