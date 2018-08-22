from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from restaurant.models import Restaurant
from restaurant.forms import RestaurantForm

@login_required(login_url='/accounts/login/')
def index(request):
    user=User.objects.get(id=request.user.id)
    #ineffective for databases with large no of users will impelent a better search
    if user in [i.user for i in Restaurant.objects.all()]:
        return redirect('restaurant:index')
    return redirect('register:restaurant-signup')
    

@login_required(login_url='/accounts/login/')
def restaurant_signup(request):
    user=User.objects.get(id=request.user.id)
    context={'user':user}
    if request.method=="POST":
        p_form=RestaurantForm(request.POST,request.FILES)
        if p_form.is_valid():
            restaurant=p_form.save(commit=False)
            restaurant.user=user
            restaurant.save()
            return redirect('restaurant:index')
    p_form=RestaurantForm()
    context.update({"form":p_form})
    return render(request,'restaurant/profile_signup.html',context)
