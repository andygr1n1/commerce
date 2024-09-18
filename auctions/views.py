from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import AuctionListing, Bid, Category, User, Watchlist


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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

def add_listing(request):
    # print(request.user)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = Category.objects.get(id=request.POST["category"]) if request.POST["category"] else None
        owner = User.objects.get(id=request.user.id)
        listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, owner=owner)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/add_listing.html", {
            "categories": categories
        })

def listing(request, listing_id):
    # print(request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        bid = request.POST.get("bid_amount")
        print('bid',bid)
        listing = AuctionListing.objects.get(id=listing_id)
        if action == "add":
            Watchlist.objects.create(user=request.user, listing=listing)
        if action == "remove":
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
        if bid:
            if float(bid) < float(listing.current_bid or 0) or float(bid) < float(listing.starting_bid or 0):
                return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "is_watchlist": Watchlist.objects.filter(user=request.user, listing=listing).exists(),
                        "message": "Bid amount must be higher than the current bid and starting bid."
                    })
            bid = Bid(bidder=request.user, listing=listing, amount=bid)
            bid.save()
            # listing.current_bid = bid.amount
            # listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        listing = AuctionListing.objects.get(id=listing_id)
        is_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watchlist": is_watchlist
    })

