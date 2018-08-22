from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as authviews

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restaurant-sign-up$', views.restaurant_signup, name='restaurant-signup'),    
    url(r'^logout/$', authviews.logout, {"next_page": '/'}, name="logout"), 
    url(r"^accounts/password/reset/auth_password_reset_done$",views.index,name="index"),
    url(r"^accounts/password/reset/confirm/Mg/set-password/auth_password_reset_complete$",views.index,name="index")
]