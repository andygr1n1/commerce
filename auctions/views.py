from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from .models import AuctionListing, Bid, Category, User, Watchlist, Comment


def index(request):
    # active listings
    listings = AuctionListing.objects.filter(is_active=True)
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

def closed_listings(request):
    listings = AuctionListing.objects.filter(is_active=False)
    return render(request, "auctions/closed_listings.html", {
        "listings": listings,
    })


def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    listings = AuctionListing.objects.filter(id__in=[watchlist_item.listing.id for watchlist_item in watchlist])
    print('!!!',listings)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    print(category.name)
    if not category.name == "Other":
        listings = AuctionListing.objects.filter(category=category, is_active=True)
    else:
        listings = AuctionListing.objects.filter(Q(category=None) | Q(category=category), is_active=True)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

def add_listing(request):
    # print(request.user)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = Category.objects.get(id=request.POST["category"]) if request.POST["category"] else None
        owner = User.objects.get(id=request.user.id)
        listing = AuctionListing(title=title, description=description, image_url=image_url, category=category, owner=owner)
        listing.save()
        new_bid = Bid(owner=request.user, amount=starting_bid, listing=listing)
        new_bid.save()
        listing.bids.add(new_bid)
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
        comment = request.POST.get("comment")
        close_auction = request.POST.get("close-auction")

        listing = AuctionListing.objects.get(id=listing_id)

        if action == "add":
            Watchlist.objects.create(user=request.user, listing=listing)
        if action == "remove":
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
        if bid:
            first_bid = listing.bids.first().amount if listing.bids.first() else 0
            last_bid_amount = listing.bids.last().amount if listing.bids.last() else 0
            if float(bid) < float(last_bid_amount) or float(bid) < float(first_bid):
                return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "is_watchlist": Watchlist.objects.filter(user=request.user, listing=listing).exists(),
                        "message": "Bid amount must be higher than the current bid and starting bid."
                    })
            new_bid = Bid(owner=request.user, amount=bid, listing=listing)
            new_bid.save()
            listing.bids.add(new_bid)
        if comment:
            Comment.objects.create(user=request.user, listing=listing, content=comment)
        if close_auction:
            listing.is_active = False
            listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        listing = AuctionListing.objects.get(id=listing_id)
        is_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists() if request.user.is_authenticated else False
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watchlist": is_watchlist,
        "bids": Bid.objects.filter(listing=listing),
        "comments": Comment.objects.filter(listing=listing).order_by('-created_at')
    })

def redirect_to_login(request, resource):
    return HttpResponseRedirect(reverse("index"))