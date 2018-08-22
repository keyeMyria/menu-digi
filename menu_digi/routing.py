from django.conf.urls import url
from django.conf.urls import url, include
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
import restaurant.channel_urls,customers.channel_urls



# urlpatterns = [
#      url(r'^customers/(?P<restaurant_name>\w+)/table/(?P<table_id>\d+)$',consumers.OrdersConsumer,name="index"),
#     ]
channel_urlpatterns = restaurant.channel_urls.urlpatterns + customers.channel_urls.urlpatterns 

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                channel_urlpatterns
            )
        )
    )
})


