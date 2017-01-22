from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from models import Account
from forms import LoginForm

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
                        action.send(user, verb='logged in')
                        return redirect('user_profile:index', request.user.username)
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
        return redirect('bankaccounts:index', request.user.username)
