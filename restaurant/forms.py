from django import forms
from .models import Restaurant,FoodItem,FoodCategory,Table,Reviews

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name",
                  "description",
                  "address",
                  "phone_number",
                  "business_email",
                  "location",
                  "avatar"]

class  FoodItemForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.restaurant=kwargs.pop("restaurant")
        self.categories=kwargs.pop("categories")
        super(FoodItemForm,self).__init__(*args,**kwargs)
        class_choices=tuple((x.name,x.name) for x in self.categories)
        self.fields["food_category"]=forms.ChoiceField(label="Food Category",choices=class_choices)

    food_category=forms.ChoiceField(label="Food Category")

    class Meta:
        model = FoodItem
        fields=["name",
                "description",
                "availability",
                "price",
                "avatar",                
        ]
class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ["name",
                 "avatar"]
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ["table"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ["customer_name",
                "review",
                "avatar"]