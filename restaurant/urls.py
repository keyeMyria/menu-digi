from django.conf.urls import url
import restaurant.views as views 

urlpatterns = [
    url(r'^restaurant/index$',views.index,name="index"),
    url(r'^restaurant/tables$',views.tables,name="tables"),
    url(r'^restaurant/food-categories$',views.food_category,name="food-category"),
    url(r'^restaurant/orders$',views.orders,name="orders"),
    url(r'^restaurant/reviews$',views.reviews,name="reviews"),
    url(r'^restaurant/add-review$',views.add_review,name="add-review"),
    url(r'^restaurant/edit-review/(?P<review_id>\d+)$',views.edit_review,name="edit-review"),
    url(r'^restaurant/orders-records$',views.ajax_orders_records,name="ajax-orders-records"),
    url(r'^restaurant/order-item/(?P<restaurant_name>\w+)/(?P<order_id>\d+)$',views.order_item,name="order-item"),
    url(r'^restaurant/edit-profile$',views.edit_profile,name="edit-profile"),
    url(r'^restaurant/add-food$',views.add_food,name="add-food"),
    url(r'^restaurant/add-table$',views.add_table,name="add-table"),
    url(r'^restaurant/add-food-category$',views.add_food_category,name="add-food-category"),
    url(r'^restaurant/edit-food/(?P<food_id>\d+)$',views.edit_food,name="edit-food"),
    url(r'^restaurant/edit-food-category/(?P<food_category_id>\d+)$',views.edit_food_category,name="edit-food-category"),
    url(r'^restaurant/edit-table/(?P<table_id>\d+)$',views.edit_table,name="edit-table"),
   
    ]



    