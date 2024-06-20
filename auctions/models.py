from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

# Creating a validator for starting bid
def validate_bid(value):
    if value < 0 and value == 0:
        raise ValidationError

class User(AbstractUser):
    pass

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
    starting_bid = models.DecimalField(max_digits=10 ,decimal_places=2, validators=[validate_bid])
    image = models.ImageField(upload_to='media/auctions', null=True, blank=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self):
        return self.title