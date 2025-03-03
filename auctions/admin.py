from django.contrib import admin
from .models import *

class AuctionlistingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'bid', 'category')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', )
    list_editable = ('bid', 'category')
    ordering = ('title',)


class BidsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'bid')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'comments')

# Register your models here.
admin.site.register(User)
admin.site.register(Auctionlistings, AuctionlistingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)