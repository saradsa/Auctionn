from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment
from .forms import CreateListingForm

# Create your views here.


def index(request):
    allListings = Listing.objects.all().order_by("-created_at")
    bid = Bid.objects.last()
    currentUser = request.user
    return render(request, "auctions/index.html", {
        "listings": allListings,
        "bid": bid,
        "usernow": currentUser
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
                "message": "Passwards must match."
            })

        # Attempt to create a new user
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
    form = CreateListingForm()
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "form": form,
            "categories": categories
        })
    else:
        title = request.POST['title']
        detail = request.POST['detail']
        image = request.POST['image']
        price = request.POST['price']
        category = request.POST['category']

        currentUser = request.user

        newListing = Listing(
            title=title,
            detail=detail,
            image=image,
            price=price,
            category=Category(pk=category),
            owner=currentUser
        )

        newListing.save()
        return HttpResponseRedirect(reverse("index"))


def categories(request):
    allCategories = Category.objects.all()
    totalitem = []
    for category in allCategories:
        item = Listing.objects.filter(category=category)
        number = len(item)
        totalitem.append(number)
    return render(request, "auctions/categories.html", {
        "categories": allCategories,
        "totalitem": totalitem,
        "allitems": zip(allCategories, totalitem)
    })


def category_listing(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.all().filter(category=category)
    return render(request, "auctions/categorylisting.html", {
        "category": category,
        "listings": listings
    })


def detail(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    isListingInWatchlist = request.user in listing.watchlist.all()
    bids = Bid.objects.all().filter(listing=listing_id).order_by("-created_at")[:5]
    bid = Bid.objects.all().filter(listing=listing_id)
    allbids = len(bid)
    comments = Comment.objects.all().filter(listing=listing_id).order_by("-created_at")
    allcomments = len(comments)
    return render(request, "auctions/detail.html", {
        "listing": listing,
        "whobid": bids,
        "allbids": allbids,
        "comments": comments,
        "allcoments": allcomments,
        "isListingInWatchlist": isListingInWatchlist
    })


def placebid(request, listing_id):

    if request.method == "POST":
        newbid = request.POST['newbid']
        listing = Listing.objects.get(pk=listing_id)
        bids = Bid.objects.all().filter(listing=listing_id)
        allbids = len(bids)
        lastbid = Bid.objects.last()
        
        if lastbid is not None:
            lastbids = lastbid.new_bid
            if int(newbid) > int(listing.price) and int(newbid) > int(lastbids):
                newbid = Bid(
                    listing=Listing.objects.get(pk=listing_id),
                    bidder=request.user,
                    new_bid=newbid
                )
                newbid.save()
            else:
                return render(request, "auctions/detail.html", {
                    "listing": listing,
                    "message": "Place a bid higher than the existing one",
                    "whobid": bids,
                    "allbids": allbids
                })
        else:
            if int(newbid) > int(listing.price):
                newbid = Bid(
                    listing=Listing.objects.get(pk=listing_id),
                    bidder=request.user,
                    new_bid=newbid
                )
                newbid.save()
            else:
                return render(request, "auctions/detail.html", {
                    "listing": listing,
                    "message": "Place a bid higher than the existing one",
                    "whobid": bids,
                    "allbids": allbids
                })

    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.all().filter(listing=listing_id).order_by("-created_at")[:5]

    bid = Bid.objects.all().filter(listing=listing_id)
    allbid=len(bid)
    isListingInWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.all().filter(listing=listing_id).order_by("-created_at")
    allcomments = len(comments)
    return render(request, "auctions/detail.html", {
        "listing": listing,
        "whobid": bids,
        "allbids": allbid,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": comments,
        "allcoments": allcomments
    })

def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST['comment']
        currentUser = request.user
        newcomment = Comment(
            listing = Listing.objects.get(pk=listing_id),
            commenter = request.user,
            comment = comment
            )
        newcomment.save()
        listing = Listing.objects.get(pk=listing_id)
        isListingInWatchlist = request.user in listing.watchlist.all()
        bids = Bid.objects.all().filter(listing=listing_id).order_by("-created_at")[:5]
        bid = Bid.objects.all().filter(listing=listing_id)
        allbids = len(bid)
        comments = Comment.objects.all().filter(listing=listing_id).order_by("-created_at")
        allcomments = len(comments)
        return render(request, "auctions/detail.html", {
            "listing": listing,
            "comments": comments,
            "allcomments": allcomments,
            "isListingInWatchlist": isListingInWatchlist,
            "whobid": bids,
            "allbids": allbids

        })

def removeWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    currentUser = request.user
    listing.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("detail", args=(id, )))
    pass

def addWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    currentUser = request.user
    listing.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("detail", args=(id, )))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
        })
