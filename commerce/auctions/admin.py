from django.contrib import admin
from auctions.models import User,AuctionListing,bids,comments,Watchlist


# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(Watchlist)


