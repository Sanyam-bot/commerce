from django import forms

class listing(forms.Form):
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

    title = forms.CharField(label='Title' ,max_length=80)
    description = forms.CharField(label='Description', max_length=4000)
    starting_bid = forms.FloatField(label='Bid')
    # image_url = forms.URLField(label='Image URL')
    category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES)