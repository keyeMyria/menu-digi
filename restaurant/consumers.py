import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

class OrdersConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
    async def websocket_receive(self,event):
        print("receive",event)
    async def webscoket_disconnect(self,event):
        print("disconnected",event)
