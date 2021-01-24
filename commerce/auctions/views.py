from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from PIL import Image
from .models import User , AuctionListing,Watchlist,bids
from django.contrib.auth.decorators import login_required
import json
from .forms import AuctionForm

def index(request):
    if request.method == 'GET':
        listing = AuctionListing.objects.all()
        return render(request , 'auctions/index.html',{
            "AuctionListing":listing
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

@login_required
def create(request):

    ''' Create a new product '''
    listing = AuctionListing.objects.all()

    if request.method == 'POST':
        form = AuctionForm(request.POST,request.FILES,request.user)
        if form.is_valid():
            form.save()
            return render(request , 'auctions/index.html',{
            "AuctionListing":listing
        })
    else:
        form=AuctionForm()
    return render(request , 'auctions/createListing.html',{
        'form': form
    })


def view_listing(request):

    ''' List of all products'''

    if request.method == 'GET':
        listing = AuctionListing.objects.all()
        # print(listing[0].user)
        return render(request , 'auctions/index.html',{
            "AuctionListing":listing
        })

def detailed_view(request,pk):

    ''' Detailed view of a Product'''


    items_waitlist=[]
    pre_bids_total = (bids.objects.filter(auction_id = pk)).count()
    pre_bids = bids.objects.filter(auction_id = pk)
    highest_bid=0
    winner=""
    cancel_auction=False
    if(pre_bids):
        # highest_bids = bids.objects.get(auction_id = pk).last()
        highest_bids = pre_bids.last()
        highest_bid = highest_bids.bids
        highest_bidder = highest_bids.bidder_id
        # Get the highest bidder
        winner=User.objects.get(id=highest_bidder)
    
    w_whachList = Watchlist.objects.all()
    lists = AuctionListing.objects.get(pk=pk)

    if(request.user.id == lists.user_id):
        cancel_auction==True
    for _wList in w_whachList:
        data = _wList.listingid
        items_waitlist.append(data)
    if lists not in items_waitlist:     
        return render(request,"auctions/detailed_view.html",
        {
            "title":lists.title,
            "description":lists.description,
            "bid":lists.bid,
            "category":lists.category,
            "auction_id":pk,
            "added":False,
            "p_bids":pre_bids_total,
            "h_bid":highest_bid,
            "cancel_auction":cancel_auction,
            "post_createdBy":lists.user_id,
            "active":lists.active,
            "winner":winner
        }
                )
    else:
        return render(request,"auctions/detailed_view.html",
        {
            "title":lists.title,
            "description":lists.description,
            "bid":lists.bid,
            "category":lists.category,
            "auction_id":pk,
            "added":True,
            "p_bids":pre_bids_total,
            "h_bid":highest_bid,
            "cancel_auction":cancel_auction,
            "post_createdBy":lists.user_id,
            "active":lists.active,
            "winner":winner

            
        }
                )

def category(request,category):
    ''' categorywise listing '''
    category=AuctionListing.objects.filter(category=category)
    for cat in category:
    
        return render(request,"auctions/category.html",
        {
                "category":category,              
        })

@login_required
def addTowatchlist(request,auction_id):

    ''' Add product to the watchlist'''

    lists = AuctionListing.objects.get(pk=auction_id)  
    Watchlist.objects.create(listingid=lists,user=request.user)
    return render(request,"auctions/error.html",{
        "message":"Sucessfully added to watchlist"
    })
  
@login_required
def watchlist(request):

    ''' List of watchlisted items'''

    items_waitlist=[]
    lists = Watchlist.objects.filter(user=request.user)
    for _list in lists:
        data = _list.listingid
        items_waitlist.append(data)
    return render(request,"auctions/watchlist.html",{
        "watchlist":items_waitlist
    })

@login_required
def removewatchlist(request,auction_id):

    ''' Remove item from watchlist '''
    obj = Watchlist.objects.filter(listingid_id=auction_id).delete()
    return render(request,"auctions/index.html",{
    })

@login_required
def addBid(request,auction_id):

    ''' Add bids to a product'''

    pre_bids = (bids.objects.filter(auction_id = auction_id))
    auction =AuctionListing.objects.get(id=auction_id)
    if(pre_bids):
        last_bid=pre_bids.reverse()[0].bids
        if request.method == 'POST':
            if(last_bid):
                if int(request.POST['bids']) > last_bid and auction.bid:
                    bid = request.POST['bids']
                    
                    bids.objects.create(bids = request.POST['bids'],
                                        auction=(auction),
                                        bidder=request.user

                                    )
                    return render(request,"auctions/error.html",{
                        "message":"Bid added successfully!",
                        "pk":auction_id
                    })
                else:
                    return render(request,"auctions/error.html",{
                        "message":"Please entre bid greater than"+" "+str(last_bid),
                        "pk":auction_id
                    })
    else:
        if int(request.POST['bids']) > int(auction.bid):
            bid = request.POST['bids']
            
            bids.objects.create(bids = request.POST['bids'],
                                auction=(auction),
                                bidder=request.user
                            )
            return render(request,"auctions/error.html",{
                "message":"Bid added successfully!",
                "pk":auction_id
            })
        else:
            return render(request,"auctions/error.html",{
                "message":"Please entre bid greater than"+""+"$"+str(auction.bid),
                "pk":auction_id
            })

        
    return render(request,"auctions/index.html")



@login_required
def endAuction(request,auction_id):
    ''' End a product's auction '''
    auction = AuctionListing.objects.get(id=auction_id)
    auction.active=False
    auction.save()
    return render(request,"auctions/index.html",{

    })





