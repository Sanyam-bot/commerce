from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

# Creating a validator for starting bid
def validate_bid(value):
    if value < 0 and value == 0:
        raise ValidationError

class User(AbstractUser):
    watchlist = models.ManyToManyField('Auctionlistings', related_name='users_watchlist')

class Auctionlistings(models.Model):
    # The key is what gets store and value is human-readable
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=4000)
    bid = models.DecimalField(max_digits=10 ,decimal_places=2, validators=[validate_bid])
    # image = models.ImageField(upload_to='media/auctions', null=True, blank=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, blank=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='won_auctions')
    
    def save(self, *args, **kwargs):
        if self.winner is not None:
            self.active = False
        super(Auctionlistings, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids_user')
    listing = models.ForeignKey(Auctionlistings, on_delete=models.CASCADE, related_name='listing_bids')
    bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_bid])

    def __str__(self):
        return str(self.bid) # Used str cause the return value had to be a string
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    listing = models.ForeignKey(Auctionlistings, on_delete=models.CASCADE, related_name='listing_comments')
    comments = models.CharField(max_length=40000)

    def __str__(self):
        return self.comments 