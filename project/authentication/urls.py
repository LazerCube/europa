from django.conf.urls import include, url
from . import views

app_name = 'authentication'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
]
