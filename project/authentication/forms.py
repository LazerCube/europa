from django import forms
from authentication.models import Account

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'id' : 'inputUsername',
                                                             'class' : 'form-input',
                                                             'placeholder' : 'Email',
                                                             'autocomplete' : 'off'}),
                                                             max_length=100)
    password= forms.CharField(widget=forms.PasswordInput(attrs={'id' : 'inputPassword',
                                                             'class' : 'form-input',
                                                             'placeholder' : 'Password'}))
