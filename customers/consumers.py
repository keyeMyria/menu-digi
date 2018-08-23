import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core.serializers import serialize
from django.db import close_old_connections
from restaurant.models import Restaurant, FoodItem,FoodCategory,Table,Order

class OrdersConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
        await self.send({
            "type":"websocket.accept"
        })
        self.user=self.scope["user"]
        self.restaurant_name=self.scope["url_route"]["kwargs"]["restaurant_name"]
        # self.table_id = self.scope["url_route"]["kwargs"]["table_id"]
        state = await self.validate_connection()
        if not state:
            return  await self.send({"type":"websocket.close"})
        if self.user == self.restaurant.user:
            await self.channel_layer.group_add(
                self.restaurant.name, 
                self.channel_name
            )

    async def websocket_receive(self,event):
        print("received:",event["text"])
        data= json.loads(event["text"])
        if data["event"]=="Order":
            state,message= await self.validate_order(data)
            if not state:
                return await self.send({
                "type":"websocket.send",
                "text": json.dumps({"status":state,"message":message})
            })
            self.order_data= serialize("json",[self.order,])
            await self.channel_layer.group_send(
                self.restaurant.name,
                {
                    'type': 'chat_message',
                    'message': self.order_data
                }
            )
            await self.send({
                "type":"websocket.send",
                "text": json.dumps({"status":state,"message":message})
            })

    async def websocket_disconnect(self,event):
        print("disconnected",event)


    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["message"]
        })

    @database_sync_to_async
    def validate_connection(self):
        try:
            close_old_connections()
            self.restaurant=Restaurant.objects.get(name=self.restaurant_name)
            close_old_connections()
            # self.table=Table.objects.get(pk=self.table_id,restaurant=self.restaurant)
            return True
        except Exception as err:
            print("Error:",err)
            return False

    @database_sync_to_async
    def validate_order(self,data):
        try:
            username=data["username"]
            if username=="":
                return False,"Username is required"
            email=data["email"]
            if not email:
                return False,"email is required"
            message=data["message"]
            phone_number=data["contact"]
            if not phone_number:
                return False,"phone number is required"
            order_info=data["foods"]
            if not order_info:
                return False,"Order item(s) required"
            tableId=data["table"]
            self.table=Table.objects.get(pk=tableId,restaurant=self.restaurant)
            order=Order(username=username,
                        email=email,
                        phone_number=phone_number,
                        additional_info=message,
                        order_info=order_info,
                        restaurant=self.restaurant,
                        table=self.table)
            order.set_time_str()
            order.save()
            self.order = order
            return True,"Order added successfully, please wait"
        except Exception as err:
            print(err)
            return False,"An error occured, please try again"
