from django.contrib import admin
from .models import Restaurant
admin.site.register(
    Restaurant,
    list_display=["name"]

)

# Register your models here.
