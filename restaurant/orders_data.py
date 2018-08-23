from django.contrib.auth.models import User
import json
from restaurant.models import *
from django import forms

class Ajax(forms.Form):
    args = []
    user = []
    def __init__(self, *args, **kwargs):
        self.args = args
        if len(args) > 1:
            self.user = args[1]
        if self.user.id == None:
            self.user = "NL"

    def error(self, message):
        return json.dumps({ "Status": "Error", "Message": message }, ensure_ascii=False)

    def success(self, message):
        return json.dumps({ "Status": "Success", "Message": message }, ensure_ascii=False)

    def items(self, json):
        return json

    def output(self):
        return self.validate()

class AjaxOrdersRecords(Ajax):
    def validate_order(self,order):
        try:
            if order.username=="" or order.phone_number=="" or order.get_total_cost() <= 0 or not order.order_info or not order.time_description:
                return False
            return True
        except Exception as err:
            print(err)
            return False

    def validate(self):
        try:
            self.restaurant_name = self.args[0]["restaurant"]
        except Exception as e:
            return self.error("Malformed request, did not process.")
        try:
            self.restaurant = Restaurant.objects.get(name=self.restaurant_name)
        except:
            return self.error("Invalid restaurant name.")
        

        records=Order.objects.filter(restaurant=self.restaurant).order_by("-created_at")
        r=[]
        if records:
            for item in records: 
                if self.validate_order(item):
                    r.append({
                    "id": item.pk,
                    "table": item.table.table, 
                    "contact": item.phone_number, 
                    "cost": "Ksh.{}".format(item.get_total_cost()),
                    "time": item.time_description})
            return self.items(json.dumps(r))
        else:
            return self.error("No records found")

        