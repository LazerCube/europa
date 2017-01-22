from django import forms
from django.contrib.auth.password_validation import validate_password

from authentication.models import Account

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'id' : 'inputUsername',
                                                             'class' : 'form-control',
                                                             'placeholder' : 'Email',
                                                             'autocomplete' : 'off'}),
                                                             max_length=100)
    password= forms.CharField(widget=forms.PasswordInput(attrs={'id' : 'inputPassword',
                                                             'class' : 'form-control',
                                                             'placeholder' : 'Password'}))

class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.TextInput(attrs={'id' : 'inputEmail',
                                                            'class' : 'form-control',
                                                            'placeholder' : 'Email',
                                                            'autocomplete' : 'off'}),
                                                            max_length=100)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'id' : 'inputPassword',
                                                                'class' : 'form-control',
                                                                'placeholder' : 'Password'}))


    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id' : 'inputConfirmPassword',
                                                                        'class' : 'form-control',
                                                                        'placeholder' : 'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['email',
                'password',
                'confirm_password',
                ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('The Email, %s is already in use.' % email)
        return email

    def clean(self):
        """
        Checks if the passwords match
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
            validate_password(self.cleaned_data.get('confirm_password'), self.instance)
        return self.cleaned_data
