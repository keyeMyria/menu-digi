from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages

import json
from restaurant.models import Restaurant, FoodItem,FoodCategory,Table,Order

def index(request,restaurant_name,table_id):
    restaurant=get_object_or_404(Restaurant,name=restaurant_name)
    table=get_object_or_404(Table,restaurant=restaurant,table=table_id)
    context={"restaurant":restaurant,
            "table":table}
    return render(request,"customer/index.html",context)







