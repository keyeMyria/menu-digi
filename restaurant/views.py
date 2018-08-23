from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings 
from django.urls import reverse
from django.db import close_old_connections

from .forms import FoodItemForm,FoodCategoryForm,RestaurantForm,TableForm,ReviewForm
from .orders_data import AjaxOrdersRecords
from .models import Restaurant, FoodItem,FoodCategory,Table,Order,Reviews
from collections import defaultdict


@login_required(login_url='/accounts/login/')
def index(request):
    profile=get_object_or_404(Restaurant,user=request.user)

    ##get food items & categories
    food_categories_dict={i.id:i for i in FoodCategory.objects.filter(restaurant=profile)}
    food_list_dict= {i:i.category_id for i in FoodItem.objects.filter(restaurant=profile)}
    # sol to avoid hitting the database multiple times
    x=defaultdict(list)
    l={}
    for k,v in food_list_dict.items():
        x[food_categories_dict[v]].append(k)
    for k,v in x.items():
        if len(v)>0:
            l.update({k:v})
    context={'profile':profile,"sorted_food":l}
    return render(request,"restaurant/index.html",context)

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    context={'profile':profile,}
    if request.method=="POST":
        d_form=RestaurantForm(request.POST,request.FILES,instance=profile)
        if d_form.is_valid():
            d_changes=d_form.save(commit=True)
            messages.info(request,"Profile Edited successfully")
            return redirect("restaurant:index")
    d_form=RestaurantForm(instance=profile)
    context.update({"form":d_form})
    return render(request,'restaurant/edit-profile.html',context)

@login_required(login_url='/accounts/login/')
def add_food(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    context={'profile':profile,}
    food_categories=FoodCategory.objects.filter(restaurant=profile)
    if not food_categories:
        _=FoodCategory.objects.get_or_create(restaurant=profile,name="General")

    if request.method=="POST":
        food_form=FoodItemForm(request.POST,request.FILES,restaurant=profile,categories=food_categories)
        if food_form.is_valid():
            food=food_form.save(commit=False)
            try:
                c=food_form.cleaned_data["food_category"]
                f_cat=FoodCategory.objects.filter(name=c,restaurant=profile)[0]
            except:
                f_cat=FoodCategory.objects.get_or_create(restaurant=profile,name="General")
            food.category=f_cat
            food.restaurant=profile
            food.save()
            messages.info(request,"Food added successfully")
            return redirect("restaurant:index")

    food_form=FoodItemForm(restaurant=profile,categories=food_categories)
    context.update({"form":food_form})
    return render(request,'restaurant/add-food.html',context)

@login_required(login_url='/accounts/login/')
def edit_food(request,food_id):
    profile=get_object_or_404(Restaurant, user=request.user)
    food=get_object_or_404(FoodItem, id=food_id,restaurant=profile)
    food_categories=FoodCategory.objects.filter(restaurant=profile)
    context={'profile':profile,"food":food}
    if request.method=="POST":
        food_form=FoodItemForm(request.POST,request.FILES,instance=food,restaurant=profile,categories=food_categories)
        if food_form.is_valid():
            food=food_form.save(commit=False)
            try:
                c=food_form.cleaned_data["food_category"]
                f_cat=FoodCategory.objects.filter(name=c,restaurant=profile)[0]
            except:
                f_cat=FoodCategory.objects.get_or_create(restaurant=profile,name="General")
            food.category=f_cat
            food.save()
            messages.info(request,"Food Edited successfully")
            return redirect("restaurant:index")
    food_form=FoodItemForm(instance=food,restaurant=profile,categories=food_categories)
    context.update({"form":food_form})
    return render(request,'restaurant/edit-food.html',context)
  
@login_required(login_url='/accounts/login/')
def add_food_category(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    context={'profile':profile}
    if request.method=="POST":
        food_category_form=FoodCategoryForm(request.POST,request.FILES)
        if food_category_form.is_valid():
            food_category=food_category_form.save(commit=False)
            try:
                _=FoodCategory.objects.get(restaurant=profile,name=food_category.name)
                messages.error(request,"Food category with that name already exists")
                return redirect("restaurant:add-food-category")
            except ObjectDoesNotExist:
                food_category.restaurant=profile
                food_category.save()
            return redirect('restaurant:food-category')
    food_category_form=FoodCategoryForm()
    context.update({"form":food_category_form})
    return render(request,'restaurant/add-food-category.html',context)

@login_required(login_url='/accounts/login/')
def edit_food_category(request,food_category_id):
    profile=get_object_or_404(Restaurant, user=request.user)
    food_category=get_object_or_404(FoodCategory, id=food_category_id,restaurant=profile)
    context={'profile':profile,"food_category":food_category}
    if request.method=="POST":
        food_category_form=FoodCategoryForm(request.POST,request.FILES,instance=food_category)
        if food_category_form.is_valid():
            food_category=food_category_form.save()
            messages.info(request,"Food Category Edited successfully")
            return redirect("restaurant:food-category")
    food_category_form=FoodCategoryForm(instance=food_category)
    context.update({"form":food_category_form})
    return render(request,'restaurant/edit-food-category.html',context)

@login_required(login_url='/accounts/login/')
def add_table(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    context={'profile':profile}
    if request.method=="POST":
        table_form=TableForm(request.POST)
        if table_form.is_valid():
            table=table_form.save(commit=False)
            try:
                _=Table.objects.get(restaurant=profile,table=table.table)
                messages.error(request,"Table with that id already exists")
                return redirect("restaurant:add-table")
            except:
                pass
            table.restaurant=profile
            table.save()
            messages.info(request,"Table added successfully")
            return redirect("restaurant:tables")
    table_form=TableForm()
    context.update({"form":table_form})
    return render(request,'restaurant/add-table.html',context)

@login_required(login_url='/accounts/login/')
def edit_table(request,table_id):
    profile=get_object_or_404(Restaurant, user=request.user)
    table_=get_object_or_404(Table, id=table_id,restaurant=profile)
    intial_table_id=table_.table
    context={'profile':profile,"table":table_}
    if request.method=="POST":
        table_form=TableForm(request.POST,instance=table_)
        if table_form.is_valid():
            table=table_form.save(commit=False)
            if table.table != intial_table_id and Table.objects.filter(restaurant=profile,table=table.table):
                messages.error(request,"Table with that id already exists")
                return redirect("restaurant:edit-table",table_id=table_id)
            table.save()
            messages.info(request,"Table Edited successfully")
            return redirect("restaurant:tables")
    table_form=TableForm(instance=table_)
    context.update({"form":table_form})
    return render(request,'restaurant/edit-table.html',context)

@login_required(login_url='/accounts/login/')
def tables(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    tables=Table.objects.filter(restaurant=profile)
    context={'profile':profile,"tables":tables}
    return render(request,"restaurant/tables.html",context)

@login_required(login_url='/accounts/login/')
def food_category(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    food_categories=FoodCategory.objects.filter(restaurant=profile)
    context={'profile':profile,"food_categories":food_categories}
    return render(request,"restaurant/food-category.html",context)


def ajax_orders_records(request):
    ajax = AjaxOrdersRecords(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)

@login_required(login_url='/accounts/login/')
def orders(request):
    profile=get_object_or_404(Restaurant,user=request.user)
    table_headers=["Table","Contact","Cost","Time","View"]
    context={'profile':profile,"table_headers":table_headers}
    return render(request,"restaurant/orders.html",context)

@login_required(login_url='/accounts/login/')
def order_item(request,restaurant_name,order_id):
    profile=get_object_or_404(Restaurant,user=request.user)
    order=get_object_or_404(Order,pk=order_id)
    order_details=[]
    food_items={ i.pk:i for i in FoodItem.objects.filter(restaurant=profile)}
    for i in order.order_info:
        food=food_items[int(i["id"])]
        order_details.append({"name":food.name,"price":food.price,"quantity":i["quantity"],"total":int(i["quantity"])*food.price})
    context={"profile":profile,"order":order,"order_details":order_details}
    return render(request,"restaurant/order-item.html",context)

@login_required(login_url='/accounts/login/')
def add_review(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    context={'profile':profile,}
    if request.method=="POST":
        review_form=ReviewForm(request.POST)
        if review_form.is_valid():
            review=review_form.save(commit=False)
            review.restaurant=profile
            review.save()
            messages.info(request,"Review added successfully")
            return redirect("restaurant:reviews")
    review_form=ReviewForm()
    context.update({"form":review_form})
    return render(request,'restaurant/add-review.html',context)

@login_required(login_url='/accounts/login/')
def edit_review(request,review_id):
    profile=get_object_or_404(Restaurant, user=request.user)
    review_=get_object_or_404(Reviews, id=review_id,restaurant=profile)
    context={'profile':profile,
            'user':user,"review":review_}
    if request.method=="POST":
        review_form=ReviewForm(request.POST,instance=review_)
        if review_form.is_valid():
            review_form.save()
            messages.info(request,"Review Edited successfully")
            return redirect("restaurant:reviews")
    review_form=ReviewForm(instance=review_)
    context.update({"form":review_form})
    return render(request,'restaurant/edit-review.html',context)

@login_required(login_url='/accounts/login/')
def reviews(request):
    profile=get_object_or_404(Restaurant, user=request.user)
    context={'profile':profile}
    reviews=Reviews.objects.filter(restaurant=profile)
    return render(request,"restaurant/reviews.html",context)