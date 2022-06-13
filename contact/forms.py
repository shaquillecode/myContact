'''Forms'''
from django import forms

class LoginForm(forms.Form):
    '''Form for Log in'''
    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(label="password", max_length=30)

class AddressForm(forms.Form):
    '''Form for Address'''
    address = forms.CharField(label="Address", max_length=30)
    city = forms.CharField(label="City", max_length=30)
    state = forms.CharField(label="State", max_length=30)
    country = forms.CharField(label="Country", max_length=30)
    zip_code = forms.CharField(label="Zip Code", max_length=30)
