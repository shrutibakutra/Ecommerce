from django.forms import ModelForm
from .models import AuctionListing
from django import forms

class AuctionForm(ModelForm):
    class Meta:
        model= AuctionListing
        fields = ('user','title','description','bid','image','category','active')

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'bid':forms.TextInput(attrs={'class':'form-control'}),

        }