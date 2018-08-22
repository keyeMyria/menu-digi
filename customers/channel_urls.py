from django.conf.urls import url
import customers.consumers as consumers

urlpatterns = [
     url(r'^customers/(?P<restaurant_name>\w+)$',consumers.OrdersConsumer,name="index"),
    ]