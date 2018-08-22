from django.conf.urls import url
import customers.views as views 

urlpatterns = [
     url(r'^customers/(?P<restaurant_name>\w+)/table/(?P<table_id>\d+)$',views.index,name="index"),
    ]