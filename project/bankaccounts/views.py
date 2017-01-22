from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin,
)
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.shortcuts import render

from models import BankAccount

class BankAccountListView(LoginRequiredMixin, generic.ListView):
    model = BankAccount
    template_name = 'bankaccounts/list_view.html'

    def get_queryset(self):
        return BankAccount.objects.get_user_bankaccounts(self.request.user)
