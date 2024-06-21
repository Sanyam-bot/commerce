from django.contrib import admin
from .models import User, Auctionlistings, Bids

class AuctionlistingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'starting_bid', 'category')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', )
    list_editable = ('starting_bid', 'category')
    ordering = ('title',)


class BidsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'bid')


# Register your models here.
admin.site.register(User)
admin.site.register(Auctionlistings, AuctionlistingsAdmin)
admin.site.register(Bids, BidsAdmin)