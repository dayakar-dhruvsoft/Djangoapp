from django.urls import path
from django.conf.urls import url

from .views import HomePageView,login,callback

urlpatterns = [
    path('', HomePageView, name='home'),
	url(r'^login/$',login),
	url(r'^callback/$',callback)
]