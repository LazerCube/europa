from django.conf.urls import include, url
from . import views

app_name = 'authentication'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
]
