from django.db import models
from django.contrib.postgres.fields import ArrayField
from menu_digi.cloud_fix import CloudinaryFieldFix
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from datetime import datetime
import pytz

# Create your models here.


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255,blank=False, null=True,unique=True)
    description=models.CharField(max_length=255,blank=False, null=True)
    address=models.CharField(max_length=255,blank=False, null=True)
    phone_number=models.CharField(max_length=255,blank=False, null=True)
    business_email=models.CharField(max_length=255,blank=False, null=True)
    location=models.CharField(max_length=255,blank=False, null=True)
    avatar = CloudinaryFieldFix("image",blank=True, null=True)


    def __str__(self):
        return "{}".format(self.name)

class FoodCategory(models.Model):
    name=models.CharField(max_length=255,default="General")
    restaurant=models.ForeignKey('Restaurant', related_name='food_category', on_delete=models.CASCADE, null=True)
    avatar=CloudinaryFieldFix("image",blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)
    
class FoodItem(models.Model):
    AVAILABILITY_CHOICES = ((True, 'Available'),(False, 'Unavailable'))
    restaurant=models.ForeignKey('Restaurant', related_name='food', on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=False, null=True)
    description=models.CharField(max_length=255,blank=False, null=True)
    availability=models.BooleanField(choices=AVAILABILITY_CHOICES,default=False)
    category=models.ForeignKey('FoodCategory', related_name='food', on_delete=models.CASCADE,blank=False, null=True)
    price=models.PositiveIntegerField(blank=False, null=True)
    avatar=CloudinaryFieldFix("image",blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

class Table(models.Model):
    restaurant=models.ForeignKey('Restaurant', related_name='table', on_delete=models.CASCADE,blank=False, null=True)
    table=models.PositiveIntegerField(blank=False, null=True)
    def __str__(self):
        return "Table: {}".format(self.pk)

class Order(models.Model):
 
    STATUS_CHOICES = ((True, 'Complete'),(False, 'Incomplete'))
    restaurant=models.ForeignKey('Restaurant', related_name='order', on_delete=models.CASCADE, null=True)
    table=models.ForeignKey('Table', related_name='order', on_delete=models.CASCADE)
    username=models.CharField(max_length=255,blank=False, null=True)
    phone_number=models.CharField(max_length=255,blank=False, null=True)
    email=models.CharField(max_length=255,blank=False, null=True)
    additional_info=models.CharField(max_length=255,blank=False, null=True)
    order_info=JSONField(null=True)
    status = models.BooleanField(choices=STATUS_CHOICES,default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # @todo remove this field
    time_description=models.CharField(max_length=255, null=True)

    def __str__(self):
        return "order:{} table {}".format(self.pk,self.table)

    def set_time_str(self):
        c_time=datetime.now(pytz.timezone(settings.TIME_ZONE))
        self.time_description=str(c_time.strftime("%Y-%m-%d %H:%M"))

    def get_total_cost(self):
        cost=0
        try:
            for i in self.order_info:
                cost += i["price"]*i["quantity"]
            return cost
        except:
            return cost


class Reviews(models.Model):
    restaurant=models.ForeignKey('Restaurant', related_name='reviews', on_delete=models.CASCADE, null=True)
    customer_name=models.CharField(max_length=255,blank=False, null=True,unique=True)
    review=models.TextField(max_length=255,blank=False, null=True,unique=True)
    avatar=CloudinaryFieldFix("image",blank=True, null=True)
