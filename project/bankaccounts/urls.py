from django.conf.urls import include, url
from . import views

app_name = 'bankaccounts'
urlpatterns = [
    url(r'^$', views.BankAccountListView.as_view(), name='index'),
]
