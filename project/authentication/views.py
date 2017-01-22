from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from models import Account
from forms import LoginForm, RegistrationForm

def register(request):
    if not request.user.is_authenticated():
        form = RegistrationForm()
        email = ''
        password = ''
        confirm_password = ''

        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']

                account = Account.objects.create_user(email=email, password=confirm_password)

                return redirect('authentication:login')

        context = {
                'form': form,
                'title':'Register',
        }

        return render(request, 'authentication/forms/register_form.html', context)
    else:
        return redirect('authentication:login', request.user.username)

def login(request):
    if not request.user.is_authenticated():
        form = LoginForm()
        username = ''
        password = ''
        state = ''
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return redirect('bankaccounts:index')
                    else:
                        state = "Your account is not active, please contact the administrator."
                else:
                    state = "Your username and/or password were incorrect."

        context = {
                'state': state,
                'username': username,
                'form': form,
                'title':'Login',
        }

        return render(request, 'authentication/forms/login_form.html', context)
    else:
        return redirect('bankaccounts:index')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('authentication:login')
