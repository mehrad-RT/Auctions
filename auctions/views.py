from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    activity = Listing.objects.filter(activity = True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": activity,
        "categories": categories
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

def makeListing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST['title']
        image = request.POST['image']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        categoryContent = Category.objects.get(name=category)
        
        bid = Bid(bid=int(price), user=user)
        bid.save()
        
        listing = Listing(owner=user, title=title, image=image, description=description, price=bid, category=categoryContent)
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Category.objects.all()
        return render(request, "auctions/makeListing.html", {
            "categories": categories
        })
    
def selected_category(request):
    if request.method == "POST":
        SubmittedCategory = request.POST["category"]
        category = Category.objects.get(name = SubmittedCategory)
        activity = Listing.objects.filter(activity = True , category = category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": activity,
            "categories": categories
        })

def listing(request , id):
    listing = Listing.objects.get(pk=id)
    listingInWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    IsThisUserTheOwner = request.user.username == listing.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "listingInWatchlist": listingInWatchlist,
        "comments": comments,
        "IsThisUserTheOwner": IsThisUserTheOwner
    })

def showWatchlist(request):
    user = request.user
    listings = user.watchlistUser.all()
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

def removeFromWatchlist(request , id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))
 
def addToWatchlist(request , id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addToComment(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    comment = request.POST["newComment"]

    newComment = Comment(author= user, listing= listing, comment= comment)

    newComment.save()

    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addToBid(request, id):
    listing = Listing.objects.get(pk=id)
    bid = request.POST["newBid"]
    if int(bid) > listing.price.bid:
        updateBid = Bid(user= request.user , bid=int(bid))
        updateBid.save()
        listing.price = updateBid
        listing.save()
        return render(request, "auctions/listing.html",{
            "message": "We are agree with your suggestion bid",
            "listing": listing,
            "acceptance": True
        })
    else:
        return render(request, "auctions/listing.html",{
            "message": "We are NOT agree with your suggestion bid",
            "listing": listing,
            "acceptance": False
        })
    
def closeAuction(request, id):
    listing = Listing.objects.get(pk=id)
    IsThisUserTheOwner = request.user.username == listing.owner.username
    listingInWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    listing.activity = False
    listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "listingInWatchlist": listingInWatchlist,
        "IsThisUserTheOwner": IsThisUserTheOwner,
        "comments": comments,
        "message": "Your Auction Is Closed 'Congratulations'",
        "acceptance": True
    })