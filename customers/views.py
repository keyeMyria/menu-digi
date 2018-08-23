from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
from collections import defaultdict

import json
from restaurant.models import Restaurant, FoodItem,FoodCategory,Table,Order,Reviews

def index(request,restaurant_name,table_id):
	restaurant=get_object_or_404(Restaurant,name=restaurant_name)
	table=get_object_or_404(Table,restaurant=restaurant,table=table_id)

	##get food items & categories
	food_categories_dict={i.id:i for i in FoodCategory.objects.filter(restaurant=restaurant)}
	food_list_dict= {i:i.category_id for i in FoodItem.objects.filter(restaurant=restaurant)}
	# sol to avoid hitting the database multiple times
	x=defaultdict(list)
	l={}
	for k,v in food_list_dict.items():
			x[food_categories_dict[v]].append(k)
	for k,v in x.items():
			if len(v)>0:
					l.update({k:v})
	active_category = list(x)[0] if len(x) != 0 else None
	reviews= Reviews.objects.filter(restaurant=restaurant)
	active_review = reviews[0] if len(reviews) > 0 else None
	context={"restaurant":restaurant,"table":table,"sorted_food":l,
	"active_category":active_category,"reviews":reviews,"active_review":active_review}
	return render(request,"customer/index.html",context)







