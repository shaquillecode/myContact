'''Form for Username and Password'''
from django import forms

class FormInscription(forms.Form):
    '''Form_inscription'''
    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(label="password", max_length=30)
