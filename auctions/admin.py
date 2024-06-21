from django.contrib import admin
from .models import User, Auctionlistings

class AuctionlistingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'starting_bid', 'category')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', )
    list_editable = ('starting_bid', 'category')
    ordering = ('title',)

# Register your models here.
admin.site.register(User)
admin.site.register(Auctionlistings, AuctionlistingsAdmin)
