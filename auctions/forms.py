from django import forms
from .models import Category


categories = Category.objects.all()


class CreateListingForm(forms.Form):

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width: 300px;', 'required': 'True'}), label="Enter Title", max_length=30)

    detail = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'required': 'True'}),
        label="Enter Product Description", max_length=300)

    image = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': 'True'}), label="Enter Image URL", max_length=1000)

    price = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'style': 'width: 300px;', 'required': 'True'}), label="Enter starting bid")
